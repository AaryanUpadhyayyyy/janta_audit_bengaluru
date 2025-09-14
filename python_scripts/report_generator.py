#!/usr/bin/env python3
"""
Report Generator for Janata Audit Bengaluru
Generates comprehensive analysis reports using free APIs and AI analysis
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
import base64
from io import BytesIO

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ReportGenerator:
    """Generate comprehensive analysis reports"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_templates()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('report_generator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_templates(self):
        """Setup HTML templates for reports"""
        self.html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            line-height: 1.6; 
            color: #333;
            background: #f8f9fa;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 10px; 
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 30px; 
            text-align: center; 
        }
        .header h1 { 
            margin: 0; 
            font-size: 2.5rem; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3); 
        }
        .header p { 
            margin: 10px 0 0 0; 
            font-size: 1.2rem; 
            opacity: 0.9; 
        }
        .content { 
            padding: 30px; 
        }
        .section { 
            margin-bottom: 40px; 
            padding: 20px; 
            border-left: 5px solid #3498db; 
            background: #f8f9fa; 
            border-radius: 0 10px 10px 0; 
        }
        .section h2 { 
            color: #2c3e50; 
            margin-bottom: 20px; 
            font-size: 1.8rem; 
        }
        .section h3 { 
            color: #34495e; 
            margin-bottom: 15px; 
            font-size: 1.4rem; 
        }
        .metrics-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin: 20px 0; 
        }
        .metric-card { 
            background: white; 
            padding: 20px; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            text-align: center; 
        }
        .metric-value { 
            font-size: 2rem; 
            font-weight: bold; 
            color: #3498db; 
            margin-bottom: 5px; 
        }
        .metric-label { 
            color: #7f8c8d; 
            font-size: 0.9rem; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
        }
        .status-badge { 
            display: inline-block; 
            padding: 8px 16px; 
            border-radius: 20px; 
            font-weight: bold; 
            font-size: 0.9rem; 
        }
        .status-completed { 
            background: #d4edda; 
            color: #155724; 
        }
        .status-progress { 
            background: #cce5ff; 
            color: #004085; 
        }
        .status-pending { 
            background: #fff3cd; 
            color: #856404; 
        }
        .status-cancelled { 
            background: #f8d7da; 
            color: #721c24; 
        }
        .chart-container { 
            margin: 20px 0; 
            text-align: center; 
        }
        .chart-container img { 
            max-width: 100%; 
            height: auto; 
            border-radius: 10px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
        }
        .recommendations { 
            background: #fff3cd; 
            border: 1px solid #ffeaa7; 
            border-radius: 10px; 
            padding: 20px; 
            margin: 20px 0; 
        }
        .recommendations h3 { 
            color: #856404; 
            margin-bottom: 15px; 
        }
        .recommendations ul { 
            margin: 0; 
            padding-left: 20px; 
        }
        .recommendations li { 
            margin-bottom: 8px; 
            color: #856404; 
        }
        .confidence-bar { 
            width: 100%; 
            height: 25px; 
            background: #e9ecef; 
            border-radius: 12px; 
            overflow: hidden; 
            margin: 15px 0; 
        }
        .confidence-fill { 
            height: 100%; 
            background: linear-gradient(90deg, #e74c3c 0%, #f39c12 50%, #27ae60 100%); 
            transition: width 0.5s ease; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            color: white; 
            font-weight: bold; 
        }
        .table { 
            width: 100%; 
            border-collapse: collapse; 
            margin: 20px 0; 
            background: white; 
            border-radius: 10px; 
            overflow: hidden; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
        }
        .table th, .table td { 
            padding: 15px; 
            text-align: left; 
            border-bottom: 1px solid #dee2e6; 
        }
        .table th { 
            background: #f8f9fa; 
            font-weight: bold; 
            color: #2c3e50; 
        }
        .table tr:hover { 
            background: #f8f9fa; 
        }
        .footer { 
            background: #2c3e50; 
            color: white; 
            padding: 20px; 
            text-align: center; 
        }
        .footer p { 
            margin: 0; 
            opacity: 0.8; 
        }
        .apis-used { 
            background: #e8f4fd; 
            border: 1px solid #bee5eb; 
            border-radius: 10px; 
            padding: 20px; 
            margin: 20px 0; 
        }
        .apis-used h3 { 
            color: #0c5460; 
            margin-bottom: 15px; 
        }
        .api-item { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 10px 0; 
            border-bottom: 1px solid #bee5eb; 
        }
        .api-item:last-child { 
            border-bottom: none; 
        }
        .api-name { 
            font-weight: bold; 
            color: #0c5460; 
        }
        .api-status { 
            padding: 4px 12px; 
            border-radius: 15px; 
            font-size: 0.8rem; 
            font-weight: bold; 
        }
        .api-status.active { 
            background: #d4edda; 
            color: #155724; 
        }
        .api-status.limited { 
            background: #fff3cd; 
            color: #856404; 
        }
        @media (max-width: 768px) {
            .container { 
                margin: 10px; 
                border-radius: 0; 
            }
            .header h1 { 
                font-size: 2rem; 
            }
            .metrics-grid { 
                grid-template-columns: 1fr; 
            }
            .content { 
                padding: 20px; 
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <p>{{ subtitle }}</p>
            <p>Generated on {{ generation_date }}</p>
        </div>
        
        <div class="content">
            {{ content }}
        </div>
        
        <div class="footer">
            <p>Generated by Janata Audit Bengaluru - AI-Powered Project Analysis</p>
            <p>Using Free APIs: OpenStreetMap, Esri World Imagery, Nominatim, Computer Vision</p>
        </div>
    </div>
</body>
</html>
        """
    
    def generate_project_report(self, analysis_data: Dict[str, Any], 
                              project_data: Dict[str, Any]) -> str:
        """Generate comprehensive project analysis report"""
        try:
            self.logger.info("Generating project analysis report")
            
            # Extract key metrics
            metrics = self._extract_metrics(analysis_data, project_data)
            
            # Generate charts
            charts = self._generate_charts(analysis_data, project_data)
            
            # Create report content
            content = self._create_report_content(analysis_data, project_data, metrics, charts)
            
            # Render HTML report
            template = Template(self.html_template)
            html_report = template.render(
                title=f"Project Analysis Report - {project_data.get('projectName', 'Unknown Project')}",
                subtitle="AI-Powered Satellite Analysis Using Free APIs",
                generation_date=datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                content=content
            )
            
            self.logger.info("Project analysis report generated successfully")
            return html_report
            
        except Exception as e:
            self.logger.error(f"Error generating project report: {str(e)}")
            return self._generate_error_report(str(e))
    
    def generate_summary_report(self, projects_data: List[Dict[str, Any]]) -> str:
        """Generate summary report for multiple projects"""
        try:
            self.logger.info(f"Generating summary report for {len(projects_data)} projects")
            
            # Calculate summary statistics
            summary_stats = self._calculate_summary_stats(projects_data)
            
            # Generate summary charts
            summary_charts = self._generate_summary_charts(projects_data)
            
            # Create summary content
            content = self._create_summary_content(projects_data, summary_stats, summary_charts)
            
            # Render HTML report
            template = Template(self.html_template)
            html_report = template.render(
                title="Project Analysis Summary Report",
                subtitle=f"Analysis of {len(projects_data)} Projects Using Free APIs",
                generation_date=datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                content=content
            )
            
            self.logger.info("Summary report generated successfully")
            return html_report
            
        except Exception as e:
            self.logger.error(f"Error generating summary report: {str(e)}")
            return self._generate_error_report(str(e))
    
    def _extract_metrics(self, analysis_data: Dict[str, Any], 
                        project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key metrics from analysis data"""
        try:
            project_status = analysis_data.get('project_status', {})
            time_analysis = analysis_data.get('time_analysis', {})
            location = analysis_data.get('location', {})
            
            metrics = {
                'project_name': project_data.get('projectName', 'Unknown Project'),
                'location': f"{location.get('city', 'Unknown')}, {location.get('state', 'Unknown')}",
                'coordinates': f"{location.get('latitude', 0):.6f}, {location.get('longitude', 0):.6f}",
                'reported_status': project_status.get('reported_status', 'Unknown'),
                'detected_status': project_status.get('detected_status', 'Unknown'),
                'status_mismatch': project_status.get('mismatch', False),
                'confidence': project_status.get('confidence', 0) * 100,
                'duration_months': time_analysis.get('total_duration_months', 0),
                'completion_percentage': time_analysis.get('completion_percentage', 0),
                'expected_completion': time_analysis.get('expected_completion', 0),
                'on_track': time_analysis.get('on_track', False),
                'analysis_confidence': analysis_data.get('confidence_score', 0) * 100,
                'analysis_timestamp': analysis_data.get('analysis_timestamp', ''),
                'recommendations': analysis_data.get('recommendations', [])
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error extracting metrics: {str(e)}")
            return {}
    
    def _generate_charts(self, analysis_data: Dict[str, Any], 
                        project_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate charts for the report"""
        try:
            charts = {}
            
            # Set style
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
            
            # 1. Project Status Comparison Chart
            fig, ax = plt.subplots(figsize=(10, 6))
            status_data = {
                'Reported': analysis_data.get('project_status', {}).get('reported_status', 'Unknown'),
                'Detected': analysis_data.get('project_status', {}).get('detected_status', 'Unknown')
            }
            
            colors = ['#3498db', '#e74c3c']
            bars = ax.bar(status_data.keys(), [1, 1], color=colors, alpha=0.7)
            ax.set_title('Project Status Comparison', fontsize=16, fontweight='bold')
            ax.set_ylabel('Status')
            ax.set_yticks([])
            
            # Add status labels
            for i, (status, bar) in enumerate(zip(status_data.values(), bars)):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, 
                       status, ha='center', va='center', fontweight='bold', fontsize=12)
            
            plt.tight_layout()
            charts['status_comparison'] = self._fig_to_base64(fig)
            plt.close(fig)
            
            # 2. Project Progress Chart
            fig, ax = plt.subplots(figsize=(10, 6))
            time_analysis = analysis_data.get('time_analysis', {})
            
            progress_data = {
                'Actual Progress': time_analysis.get('completion_percentage', 0),
                'Expected Progress': time_analysis.get('expected_completion', 0)
            }
            
            bars = ax.bar(progress_data.keys(), progress_data.values(), 
                         color=['#27ae60', '#f39c12'], alpha=0.7)
            ax.set_title('Project Progress Analysis', fontsize=16, fontweight='bold')
            ax.set_ylabel('Completion Percentage (%)')
            ax.set_ylim(0, 100)
            
            # Add percentage labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + 1, 
                       f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            charts['progress_analysis'] = self._fig_to_base64(fig)
            plt.close(fig)
            
            # 3. Confidence Score Chart
            fig, ax = plt.subplots(figsize=(8, 8))
            confidence = analysis_data.get('confidence_score', 0) * 100
            
            # Create pie chart
            sizes = [confidence, 100 - confidence]
            labels = ['Confidence', 'Uncertainty']
            colors = ['#27ae60', '#e74c3c']
            
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                            autopct='%1.1f%%', startangle=90)
            ax.set_title('Analysis Confidence Score', fontsize=16, fontweight='bold')
            
            plt.tight_layout()
            charts['confidence_score'] = self._fig_to_base64(fig)
            plt.close(fig)
            
            return charts
            
        except Exception as e:
            self.logger.error(f"Error generating charts: {str(e)}")
            return {}
    
    def _generate_summary_charts(self, projects_data: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate summary charts for multiple projects"""
        try:
            charts = {}
            
            # Set style
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
            
            # 1. Status Distribution Chart
            fig, ax = plt.subplots(figsize=(12, 6))
            
            status_counts = {}
            for project in projects_data:
                analysis = project.get('enhancedSatelliteAnalysis', {})
                status = analysis.get('project_status', {}).get('detected_status', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                bars = ax.bar(status_counts.keys(), status_counts.values(), 
                             color=['#27ae60', '#3498db', '#f39c12', '#e74c3c'])
                ax.set_title('Project Status Distribution', fontsize=16, fontweight='bold')
                ax.set_ylabel('Number of Projects')
                ax.set_xlabel('Status')
                
                # Add count labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, 
                           str(int(height)), ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            charts['status_distribution'] = self._fig_to_base64(fig)
            plt.close(fig)
            
            # 2. Confidence Score Distribution
            fig, ax = plt.subplots(figsize=(10, 6))
            
            confidence_scores = []
            for project in projects_data:
                analysis = project.get('enhancedSatelliteAnalysis', {})
                confidence = analysis.get('confidence_score', 0) * 100
                confidence_scores.append(confidence)
            
            if confidence_scores:
                ax.hist(confidence_scores, bins=10, color='#3498db', alpha=0.7, edgecolor='black')
                ax.set_title('Confidence Score Distribution', fontsize=16, fontweight='bold')
                ax.set_xlabel('Confidence Score (%)')
                ax.set_ylabel('Number of Projects')
                ax.axvline(np.mean(confidence_scores), color='red', linestyle='--', 
                          label=f'Mean: {np.mean(confidence_scores):.1f}%')
                ax.legend()
            
            plt.tight_layout()
            charts['confidence_distribution'] = self._fig_to_base64(fig)
            plt.close(fig)
            
            return charts
            
        except Exception as e:
            self.logger.error(f"Error generating summary charts: {str(e)}")
            return {}
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string"""
        try:
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            return f"data:image/png;base64,{image_base64}"
        except Exception as e:
            self.logger.error(f"Error converting figure to base64: {str(e)}")
            return ""
    
    def _create_report_content(self, analysis_data: Dict[str, Any], 
                             project_data: Dict[str, Any], 
                             metrics: Dict[str, Any], 
                             charts: Dict[str, str]) -> str:
        """Create HTML content for the report"""
        try:
            content = f"""
            <div class="section">
                <h2>📊 Project Overview</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{metrics['project_name']}</div>
                        <div class="metric-label">Project Name</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics['location']}</div>
                        <div class="metric-label">Location</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics['coordinates']}</div>
                        <div class="metric-label">Coordinates</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics['duration_months']:.1f}</div>
                        <div class="metric-label">Duration (Months)</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>🔍 Status Analysis</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">
                            <span class="status-badge status-{metrics['reported_status'].lower().replace(' ', '-')}">
                                {metrics['reported_status']}
                            </span>
                        </div>
                        <div class="metric-label">Reported Status</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">
                            <span class="status-badge status-{metrics['detected_status'].lower().replace(' ', '-')}">
                                {metrics['detected_status']}
                            </span>
                        </div>
                        <div class="metric-label">Detected Status</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{'Yes' if metrics['status_mismatch'] else 'No'}</div>
                        <div class="metric-label">Status Mismatch</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics['confidence']:.1f}%</div>
                        <div class="metric-label">Analysis Confidence</div>
                    </div>
                </div>
                
                {f'<div class="chart-container"><img src="{charts["status_comparison"]}" alt="Status Comparison"></div>' if 'status_comparison' in charts else ''}
            </div>

            <div class="section">
                <h2>⏱️ Time Analysis</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{metrics['completion_percentage']:.1f}%</div>
                        <div class="metric-label">Actual Progress</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics['expected_completion']:.1f}%</div>
                        <div class="metric-label">Expected Progress</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{'Yes' if metrics['on_track'] else 'No'}</div>
                        <div class="metric-label">On Track</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics['analysis_confidence']:.1f}%</div>
                        <div class="metric-label">Overall Confidence</div>
                    </div>
                </div>
                
                {f'<div class="chart-container"><img src="{charts["progress_analysis"]}" alt="Progress Analysis"></div>' if 'progress_analysis' in charts else ''}
            </div>

            <div class="section">
                <h2>📈 Analysis Confidence</h2>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {metrics['analysis_confidence']:.1f}%">
                        {metrics['analysis_confidence']:.1f}%
                    </div>
                </div>
                
                {f'<div class="chart-container"><img src="{charts["confidence_score"]}" alt="Confidence Score"></div>' if 'confidence_score' in charts else ''}
            </div>

            <div class="section">
                <h2>💡 Recommendations</h2>
                <div class="recommendations">
                    <h3>Key Recommendations:</h3>
                    <ul>
                        {''.join([f'<li>{rec}</li>' for rec in metrics['recommendations']])}
                    </ul>
                </div>
            </div>

            <div class="section">
                <h2>🛠️ Free APIs Used</h2>
                <div class="apis-used">
                    <h3>APIs and Services Used in This Analysis:</h3>
                    <div class="api-item">
                        <span class="api-name">OpenStreetMap</span>
                        <span class="api-status active">Active</span>
                    </div>
                    <div class="api-item">
                        <span class="api-name">Esri World Imagery</span>
                        <span class="api-status active">Active</span>
                    </div>
                    <div class="api-item">
                        <span class="api-name">Nominatim Geocoding</span>
                        <span class="api-status limited">Rate Limited</span>
                    </div>
                    <div class="api-item">
                        <span class="api-name">Computer Vision Analysis</span>
                        <span class="api-status active">Active</span>
                    </div>
                </div>
            </div>
            """
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error creating report content: {str(e)}")
            return f"<div class='section'><h2>Error</h2><p>Error generating report content: {str(e)}</p></div>"
    
    def _create_summary_content(self, projects_data: List[Dict[str, Any]], 
                               summary_stats: Dict[str, Any], 
                               summary_charts: Dict[str, str]) -> str:
        """Create HTML content for summary report"""
        try:
            content = f"""
            <div class="section">
                <h2>📊 Summary Statistics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{len(projects_data)}</div>
                        <div class="metric-label">Total Projects</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary_stats.get('completed_projects', 0)}</div>
                        <div class="metric-label">Completed Projects</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary_stats.get('in_progress_projects', 0)}</div>
                        <div class="metric-label">In Progress</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary_stats.get('average_confidence', 0):.1f}%</div>
                        <div class="metric-label">Average Confidence</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>📈 Project Status Distribution</h2>
                {f'<div class="chart-container"><img src="{summary_charts["status_distribution"]}" alt="Status Distribution"></div>' if 'status_distribution' in summary_charts else ''}
            </div>

            <div class="section">
                <h2>🎯 Confidence Score Analysis</h2>
                {f'<div class="chart-container"><img src="{summary_charts["confidence_distribution"]}" alt="Confidence Distribution"></div>' if 'confidence_distribution' in summary_charts else ''}
            </div>

            <div class="section">
                <h2>📋 Project Details</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Project Name</th>
                            <th>Status</th>
                            <th>Confidence</th>
                            <th>Progress</th>
                            <th>Location</th>
                        </tr>
                    </thead>
                    <tbody>
                        {self._create_project_table_rows(projects_data)}
                    </tbody>
                </table>
            </div>
            """
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error creating summary content: {str(e)}")
            return f"<div class='section'><h2>Error</h2><p>Error generating summary content: {str(e)}</p></div>"
    
    def _create_project_table_rows(self, projects_data: List[Dict[str, Any]]) -> str:
        """Create table rows for project data"""
        try:
            rows = []
            for project in projects_data:
                analysis = project.get('enhancedSatelliteAnalysis', {})
                project_status = analysis.get('project_status', {})
                time_analysis = analysis.get('time_analysis', {})
                location = analysis.get('location', {})
                
                status = project_status.get('detected_status', 'Unknown')
                confidence = analysis.get('confidence_score', 0) * 100
                progress = time_analysis.get('completion_percentage', 0)
                project_location = f"{location.get('city', 'Unknown')}, {location.get('state', 'Unknown')}"
                
                row = f"""
                <tr>
                    <td>{project.get('projectName', 'Unknown Project')}</td>
                    <td>
                        <span class="status-badge status-{status.lower().replace(' ', '-')}">
                            {status}
                        </span>
                    </td>
                    <td>{confidence:.1f}%</td>
                    <td>{progress:.1f}%</td>
                    <td>{project_location}</td>
                </tr>
                """
                rows.append(row)
            
            return ''.join(rows)
            
        except Exception as e:
            self.logger.error(f"Error creating table rows: {str(e)}")
            return "<tr><td colspan='5'>Error loading project data</td></tr>"
    
    def _calculate_summary_stats(self, projects_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics for multiple projects"""
        try:
            total_projects = len(projects_data)
            completed_projects = 0
            in_progress_projects = 0
            confidence_scores = []
            
            for project in projects_data:
                analysis = project.get('enhancedSatelliteAnalysis', {})
                status = analysis.get('project_status', {}).get('detected_status', 'Unknown')
                confidence = analysis.get('confidence_score', 0)
                
                if status == 'Completed':
                    completed_projects += 1
                elif status == 'In Progress':
                    in_progress_projects += 1
                
                confidence_scores.append(confidence * 100)
            
            return {
                'total_projects': total_projects,
                'completed_projects': completed_projects,
                'in_progress_projects': in_progress_projects,
                'average_confidence': np.mean(confidence_scores) if confidence_scores else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating summary stats: {str(e)}")
            return {}
    
    def _generate_error_report(self, error_message: str) -> str:
        """Generate error report"""
        return f"""
        <div class="container">
            <div class="header">
                <h1>Error Report</h1>
                <p>An error occurred while generating the report</p>
            </div>
            <div class="content">
                <div class="section">
                    <h2>Error Details</h2>
                    <p style="color: #e74c3c; font-weight: bold;">{error_message}</p>
                </div>
            </div>
        </div>
        """
    
    def save_report(self, html_content: str, filename: str) -> bool:
        """Save report to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Report saved to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving report: {str(e)}")
            return False

def main():
    """Main function for testing"""
    generator = ReportGenerator()
    
    # Sample analysis data
    sample_analysis = {
        'project_status': {
            'reported_status': 'In Progress',
            'detected_status': 'Completed',
            'confidence': 0.85,
            'mismatch': True
        },
        'time_analysis': {
            'total_duration_months': 8.5,
            'completion_percentage': 75.0,
            'expected_completion': 60.0,
            'on_track': True
        },
        'location': {
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'latitude': 12.9716,
            'longitude': 77.5946
        },
        'confidence_score': 0.82,
        'recommendations': [
            'Monitor project progress regularly',
            'Verify contractor performance',
            'Check for any unauthorized changes'
        ],
        'analysis_timestamp': datetime.now().isoformat()
    }
    
    sample_project = {
        'projectName': 'Test Road Construction',
        'description': 'Construction of new road in Bengaluru'
    }
    
    # Generate report
    html_report = generator.generate_project_report(sample_analysis, sample_project)
    
    # Save report
    filename = f"project_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    generator.save_report(html_report, filename)
    
    print(f"Report generated and saved as {filename}")

if __name__ == "__main__":
    main()
