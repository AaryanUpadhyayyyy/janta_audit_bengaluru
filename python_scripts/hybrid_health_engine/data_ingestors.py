import asyncio
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional
import aiohttp
import pandas as pd

from .base import DataIngestorInterface

class JiraIngestor(DataIngestorInterface):
    """Ingest data from Jira API"""
    
    def __init__(self, config: Dict[str, str]):
        self.base_url = config["jira_url"]
        self.auth = aiohttp.BasicAuth(config["username"], config["api_token"])
        self.project_key = config["project_key"]

    async def fetch_data(self) -> Dict:
        """Fetch project data from Jira"""
        async with aiohttp.ClientSession(auth=self.auth) as session:
            # Fetch sprint data
            sprint_url = f"{self.base_url}/rest/agile/1.0/board/{self.project_key}/sprint"
            async with session.get(sprint_url) as response:
                sprints = await response.json()

            # Fetch issue data
            issues_url = f"{self.base_url}/rest/api/2/search"
            query = {
                "jql": f"project = {self.project_key}",
                "fields": "status,customfield_10016,created,updated"  # story points field
            }
            async with session.get(issues_url, params=query) as response:
                issues = await response.json()

        return {
            "sprints": sprints["values"],
            "issues": issues["issues"]
        }

    async def validate_data(self, data: Dict) -> bool:
        """Validate fetched Jira data"""
        return (
            "sprints" in data and
            "issues" in data and
            len(data["sprints"]) > 0 and
            len(data["issues"]) > 0
        )

    async def preprocess_data(self, data: Dict) -> Dict:
        """Process raw Jira data into metrics"""
        issues_df = pd.DataFrame(data["issues"])
        sprints_df = pd.DataFrame(data["sprints"])

        # Calculate story points metrics
        total_points = issues_df["fields.customfield_10016"].sum()
        completed_points = issues_df[
            issues_df["fields.status.statusCategory.name"] == "Done"
        ]["fields.customfield_10016"].sum()

        # Calculate sprint velocity
        if len(sprints_df) >= 3:
            recent_sprints = sprints_df.sort_values("startDate", ascending=False).head(3)
            sprint_velocity = recent_sprints["completedPoints"].mean()
        else:
            sprint_velocity = completed_points / max(len(sprints_df), 1)

        return {
            "total_story_points": total_points,
            "completed_points": completed_points,
            "sprint_velocity": sprint_velocity,
            "last_updated": datetime.now().isoformat()
        }

class GitHubIngestor(DataIngestorInterface):
    """Ingest data from GitHub API"""
    
    def __init__(self, config: Dict[str, str]):
        self.token = config["github_token"]
        self.repo = config["repo"]
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def fetch_data(self) -> Dict:
        """Fetch repository data from GitHub"""
        async with aiohttp.ClientSession(headers=self.headers) as session:
            # Fetch commits
            commits_url = f"https://api.github.com/repos/{self.repo}/commits"
            async with session.get(commits_url) as response:
                commits = await response.json()

            # Fetch pull requests
            prs_url = f"https://api.github.com/repos/{self.repo}/pulls"
            async with session.get(prs_url, params={"state": "all"}) as response:
                prs = await response.json()

        return {
            "commits": commits,
            "pull_requests": prs
        }

    async def validate_data(self, data: Dict) -> bool:
        """Validate fetched GitHub data"""
        return (
            isinstance(data.get("commits"), list) and
            isinstance(data.get("pull_requests"), list)
        )

    async def preprocess_data(self, data: Dict) -> Dict:
        """Process raw GitHub data into metrics"""
        commits_df = pd.DataFrame(data["commits"])
        prs_df = pd.DataFrame(data["pull_requests"])

        # Calculate commit frequency (commits per day over last 30 days)
        if not commits_df.empty:
            recent_commits = commits_df[
                pd.to_datetime(commits_df["commit.author.date"]) > 
                pd.Timestamp.now() - pd.Timedelta(days=30)
            ]
            commit_frequency = len(recent_commits) / 30
        else:
            commit_frequency = 0

        # Calculate PR merge rate
        if not prs_df.empty:
            total_prs = len(prs_df)
            merged_prs = len(prs_df[prs_df["merged_at"].notna()])
            pr_merge_rate = merged_prs / total_prs if total_prs > 0 else 0
        else:
            pr_merge_rate = 0

        return {
            "commit_frequency": commit_frequency,
            "pr_merge_rate": pr_merge_rate,
            "last_updated": datetime.now().isoformat()
        }

class ImageIngestor(DataIngestorInterface):
    """Ingest images from various sources"""
    
    def __init__(self, config: Dict[str, str]):
        self.image_dir = Path(config["image_dir"])
        self.webcam_urls = config.get("webcam_urls", [])
        self.drone_upload_dir = Path(config.get("drone_upload_dir", ""))

    async def fetch_data(self) -> Dict:
        """Fetch images from all configured sources"""
        # Collect images from local directory
        local_images = list(self.image_dir.glob("*.{jpg,jpeg,png}"))

        # Fetch webcam images
        webcam_images = []
        async with aiohttp.ClientSession() as session:
            for url in self.webcam_urls:
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            image_data = await response.read()
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            image_path = self.image_dir / f"webcam_{timestamp}.jpg"
                            image_path.write_bytes(image_data)
                            webcam_images.append(image_path)
                except Exception as e:
                    print(f"Error fetching webcam image from {url}: {e}")

        # Collect drone footage
        drone_images = list(self.drone_upload_dir.glob("*.{jpg,jpeg,png}"))
        drone_videos = list(self.drone_upload_dir.glob("*.{mp4,avi}"))

        return {
            "local_images": [str(p) for p in local_images],
            "webcam_images": [str(p) for p in webcam_images],
            "drone_images": [str(p) for p in drone_images],
            "drone_videos": [str(p) for p in drone_videos]
        }

    async def validate_data(self, data: Dict) -> bool:
        """Validate fetched image data"""
        # Check if we have at least one valid image source
        return any(
            len(data[key]) > 0 
            for key in ["local_images", "webcam_images", "drone_images"]
        )

    async def preprocess_data(self, data: Dict) -> Dict:
        """Preprocess and organize image data"""
        all_images = []
        
        # Process and validate each image
        for source in ["local_images", "webcam_images", "drone_images"]:
            for image_path in data[source]:
                path = Path(image_path)
                if path.exists() and path.stat().st_size > 0:
                    all_images.append({
                        "path": str(path),
                        "source": source,
                        "timestamp": datetime.fromtimestamp(path.stat().st_mtime),
                        "size": path.stat().st_size
                    })

        # Sort images by timestamp
        all_images.sort(key=lambda x: x["timestamp"])

        return {
            "images": all_images,
            "video_paths": data.get("drone_videos", []),
            "last_updated": datetime.now().isoformat()
        }