#!/usr/bin/env python3
"""
Enhanced Web Server with Government Data Integration
Serves the Janata Audit platform with real-time government data updates
"""

import http.server
import socketserver
import json
import os
import threading
import webbrowser
from urllib.parse import urlparse, parse_qs
import mimetypes
from government_data_scraper import GovernmentDataScraper
from real_time_updater import start_real_time_updates, get_update_status

class EnhancedHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests with API endpoints"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # API Endpoints
        if path == '/api/government-data':
            self.serve_government_data()
        elif path == '/api/government-news':
            self.serve_government_news()
        elif path == '/api/government-schemes':
            self.serve_government_schemes()
        elif path == '/api/government-helplines':
            self.serve_government_helplines()
        elif path == '/api/government-leaders':
            self.serve_government_leaders()
        elif path == '/api/update-status':
            self.serve_update_status()
        elif path == '/api/force-update':
            self.force_government_update()
        else:
            # Serve static files
            super().do_GET()
    
    def serve_json_response(self, data):
        """Helper to serve JSON responses"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def load_government_data(self):
        """Load government data from JSON file"""
        try:
            with open('government_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            # If no data file exists, create initial data
            scraper = GovernmentDataScraper()
            return {
                'last_updated': None,
                'data': scraper.data,
                'summary': {}
            }
    
    def serve_government_data(self):
        """Serve complete government data"""
        data = self.load_government_data()
        self.serve_json_response(data)
    
    def serve_government_news(self):
        """Serve government news from all sources"""
        data = self.load_government_data()
        
        all_news = []
        gov_data = data.get('data', {})
        
        # Collect news from all sources
        for source, source_data in gov_data.items():
            news_items = source_data.get('news', [])
            for item in news_items:
                item['source_org'] = source.upper()
                all_news.append(item)
        
        # Sort by date (most recent first)
        all_news.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        response = {
            'news': all_news[:20],  # Top 20 news items
            'last_updated': data.get('last_updated'),
            'total_count': len(all_news)
        }
        
        self.serve_json_response(response)
    
    def serve_government_schemes(self):
        """Serve government schemes from all sources"""
        data = self.load_government_data()
        
        all_schemes = []
        gov_data = data.get('data', {})
        
        for source, source_data in gov_data.items():
            schemes = source_data.get('schemes', [])
            for scheme in schemes:
                scheme['source_org'] = source.upper()
                all_schemes.append(scheme)
        
        response = {
            'schemes': all_schemes,
            'last_updated': data.get('last_updated'),
            'total_count': len(all_schemes)
        }
        
        self.serve_json_response(response)
    
    def serve_government_helplines(self):
        """Serve all government helplines"""
        data = self.load_government_data()
        
        all_helplines = []
        gov_data = data.get('data', {})
        
        for source, source_data in gov_data.items():
            helplines = source_data.get('helplines', [])
            for helpline in helplines:
                helpline['source_org'] = source.upper()
                all_helplines.append(helpline)
        
        response = {
            'helplines': all_helplines,
            'last_updated': data.get('last_updated'),
            'total_count': len(all_helplines)
        }
        
        self.serve_json_response(response)
    
    def serve_government_leaders(self):
        """Serve government leaders information"""
        data = self.load_government_data()
        
        all_leaders = []
        gov_data = data.get('data', {})
        
        for source, source_data in gov_data.items():
            leaders = source_data.get('leaders', [])
            for leader in leaders:
                leader['source_org'] = source.upper()
                all_leaders.append(leader)
        
        response = {
            'leaders': all_leaders,
            'last_updated': data.get('last_updated'),
            'total_count': len(all_leaders)
        }
        
        self.serve_json_response(response)
    
    def serve_update_status(self):
        """Serve current update status"""
        status = get_update_status()
        self.serve_json_response(status)
    
    def force_government_update(self):
        """Force an immediate government data update"""
        def run_update():
            scraper = GovernmentDataScraper()
            scraper.run_scraper()
        
        # Run update in background thread
        thread = threading.Thread(target=run_update)
        thread.start()
        
        response = {
            'status': 'update_started',
            'message': 'Government data update initiated'
        }
        self.serve_json_response(response)
    
    def log_message(self, format, *args):
        """Custom log message format"""
        print(f"🌐 {format % args}")

def find_free_port(start_port=8000):
    """Find a free port starting from start_port"""
    import socket
    port = start_port
    while port < start_port + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except OSError:
                port += 1
    return None

def main():
    """Main server function"""
    print("🚀 Starting Enhanced Janata Audit Server with Government Data Integration")
    print("="*70)
    
    # Find free port
    port = find_free_port(8000)
    if not port:
        print("❌ No free ports available")
        return
    
    print(f"✅ Found free port: {port}")
    
    # Start real-time government data updates
    print("📡 Starting real-time government data updates...")
    start_real_time_updates()
    
    # Start web server
    Handler = EnhancedHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            server_url = f"http://localhost:{port}"
            
            print(f"🌐 Server running on {server_url}")
            print("✅ Server started successfully!")
            print("🌐 Features:")
            print("   • Real-time government data updates")
            print("   • BBMP, BDA, Bangalore One, Seva Sindhu integration")
            print("   • API endpoints for government data")
            print("   • Automatic data refresh every 6 hours")
            print("📝 Press Ctrl+C to stop")
            print("="*70)
            
            # Open browser
            print(f"🌐 Opening browser to: {server_url}")
            try:
                webbrowser.open(server_url)
            except:
                pass
            
            print(f"📋 If browser doesn't open automatically, copy and paste this URL:")
            print(f"   {server_url}")
            print()
            print("📊 API Endpoints:")
            print(f"   • {server_url}/api/government-data - Complete government data")
            print(f"   • {server_url}/api/government-news - Latest government news")
            print(f"   • {server_url}/api/government-schemes - Government schemes")
            print(f"   • {server_url}/api/government-helplines - All helplines")
            print(f"   • {server_url}/api/government-leaders - Government officials")
            print(f"   • {server_url}/api/update-status - Update status")
            print(f"   • {server_url}/api/force-update - Force data update")
            print("="*70)
            
            # Serve requests
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()