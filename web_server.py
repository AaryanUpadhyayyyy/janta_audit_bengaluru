#!/usr/bin/env python3
"""
Web server to serve the HTML interface and handle CORS
"""

import http.server
import socketserver
import json
import os
import subprocess
import sys
from urllib.parse import urlparse, parse_qs

class WebHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/projects':
            self.handle_projects_api()
        elif self.path == '/api/health':
            self.handle_health_api()
        elif self.path == '/':
            self.path = '/index.html'
            super().do_GET()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/scrape':
            self.handle_scrape_api()
        else:
            self.send_error(404, "Not Found")
    
    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()
    
    def handle_projects_api(self):
        """Handle /api/projects endpoint"""
        try:
            # Try to load real projects first
            if os.path.exists('real_projects.json'):
                with open('real_projects.json', 'r', encoding='utf-8') as f:
                    projects = json.load(f)
            else:
                # Fallback to mock data
                projects = get_mock_projects()
            
            response_data = {
                'success': True,
                'projects': projects,
                'total': len(projects)
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_error(500, f"Error loading projects: {str(e)}")
    
    def handle_health_api(self):
        """Handle /api/health endpoint"""
        response_data = {
            'status': 'OK',
            'message': 'Web server is running'
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())
    
    def handle_scrape_api(self):
        """Handle /api/scrape endpoint"""
        try:
            # Run the real project scraper
            result = subprocess.run([
                sys.executable, 'python_scripts/real_project_scraper.py'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # Check if real_projects.json was created
                if os.path.exists('real_projects.json'):
                    with open('real_projects.json', 'r', encoding='utf-8') as f:
                        projects = json.load(f)
                    
                    response_data = {
                        'success': True,
                        'count': len(projects),
                        'message': f'Successfully scraped {len(projects)} projects'
                    }
                else:
                    response_data = {
                        'success': False,
                        'error': 'Scraper completed but no projects file was created'
                    }
            else:
                response_data = {
                    'success': False,
                    'error': f'Scraper failed: {result.stderr}'
                }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except subprocess.TimeoutExpired:
            response_data = {
                'success': False,
                'error': 'Scraper timed out after 5 minutes'
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        except Exception as e:
            response_data = {
                'success': False,
                'error': f'Error running scraper: {str(e)}'
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())

def get_mock_projects():
    """Get mock projects data"""
    return [
        {
            'id': '1',
            'projectName': 'BBMP Road Infrastructure Development',
            'description': 'Comprehensive road development project in Ward 15',
            'status': 'In Progress',
            'budget': 50000000,
            'location': 'Bengaluru, Karnataka',
            'department': 'BBMP',
            'wardNumber': 15,
            'geoPoint': {'latitude': 12.9716, 'longitude': 77.5946},
            'contractor': 'ABC Construction Ltd.',
            'startDate': '2023-01-15',
            'endDate': '2024-12-31',
            'source': 'BBMP',
            'sourceUrl': 'https://bbmp.gov.in/',
            'scrapedAt': '2023-12-01T10:30:00Z'
        },
        {
            'id': '2',
            'projectName': 'BDA Housing Scheme Phase 2',
            'description': 'Affordable housing project for middle-income families',
            'status': 'Completed',
            'budget': 75000000,
            'location': 'Bengaluru, Karnataka',
            'department': 'BDA',
            'wardNumber': 8,
            'geoPoint': {'latitude': 12.9352, 'longitude': 77.6245},
            'contractor': 'XYZ Builders',
            'startDate': '2022-06-01',
            'endDate': '2023-11-30',
            'source': 'BDA',
            'sourceUrl': 'https://bdabangalore.org/',
            'scrapedAt': '2023-12-01T10:30:00Z'
        },
        {
            'id': '3',
            'projectName': 'BWSSB Water Supply Network',
            'description': 'New water supply network for expanding areas',
            'status': 'Pending',
            'budget': 30000000,
            'location': 'Bengaluru, Karnataka',
            'department': 'BWSSB',
            'wardNumber': 22,
            'geoPoint': {'latitude': 12.9141, 'longitude': 77.6781},
            'contractor': 'Water Works Ltd.',
            'startDate': '2024-01-01',
            'endDate': '2024-12-31',
            'source': 'BWSSB',
            'sourceUrl': 'https://bwssb.karnataka.gov.in/',
            'scrapedAt': '2023-12-01T10:30:00Z'
        },
        {
            'id': '4',
            'projectName': 'BMRCL Metro Line Extension',
            'description': 'Extension of metro line to new areas',
            'status': 'In Progress',
            'budget': 120000000,
            'location': 'Bengaluru, Karnataka',
            'department': 'BMRCL',
            'wardNumber': 12,
            'geoPoint': {'latitude': 12.9858, 'longitude': 77.6101},
            'contractor': 'Metro Construction Co.',
            'startDate': '2023-03-01',
            'endDate': '2025-06-30',
            'source': 'BMRCL',
            'sourceUrl': 'https://english.bmrc.co.in/',
            'scrapedAt': '2023-12-01T10:30:00Z'
        },
        {
            'id': '5',
            'projectName': 'BESCOM Electrical Infrastructure',
            'description': 'Upgradation of electrical infrastructure',
            'status': 'In Progress',
            'budget': 40000000,
            'location': 'Bengaluru, Karnataka',
            'department': 'BESCOM',
            'wardNumber': 18,
            'geoPoint': {'latitude': 12.9230, 'longitude': 77.5933},
            'contractor': 'Power Solutions Inc.',
            'startDate': '2023-08-01',
            'endDate': '2024-08-31',
            'source': 'BESCOM',
            'sourceUrl': 'https://bescom.karnataka.gov.in/',
            'scrapedAt': '2023-12-01T10:30:00Z'
        },
        {
            'id': '6',
            'projectName': 'KPWD Bridge Construction',
            'description': 'New bridge construction over river',
            'status': 'Pending',
            'budget': 60000000,
            'location': 'Bengaluru, Karnataka',
            'department': 'KPWD',
            'wardNumber': 25,
            'geoPoint': {'latitude': 12.9569, 'longitude': 77.7011},
            'contractor': 'Bridge Builders Ltd.',
            'startDate': '2024-02-01',
            'endDate': '2025-01-31',
            'source': 'KPWD',
            'sourceUrl': 'https://kpwd.karnataka.gov.in/',
            'scrapedAt': '2023-12-01T10:30:00Z'
        }
    ]

def main():
    # Try different ports if 8080 is blocked
    ports_to_try = [8080, 8081, 8082, 3000, 5000, 8000, 9000]
    httpd = None
    
    for PORT in ports_to_try:
        try:
            print(f"🚀 Starting Janata Audit Bengaluru Web Server")
            print(f"🌐 Trying port {PORT}...")
            
            httpd = socketserver.TCPServer(("", PORT), WebHandler)
            print(f"✅ Successfully started on port {PORT}")
            print(f"🌐 Open http://localhost:{PORT} in your browser")
            print(f"📊 API available at: http://localhost:{PORT}/api/projects")
            print(f"📝 Press Ctrl+C to stop")
            print("=" * 50)
            break
            
        except PermissionError:
            print(f"❌ Port {PORT} is blocked or in use, trying next port...")
            continue
        except OSError as e:
            print(f"❌ Port {PORT} error: {e}, trying next port...")
            continue
    
    if httpd is None:
        print("❌ Could not start server on any port. Please check your firewall settings.")
        print("💡 Try running as administrator or check if any other application is using these ports.")
        return
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        if httpd:
            httpd.server_close()

if __name__ == "__main__":
    main()
