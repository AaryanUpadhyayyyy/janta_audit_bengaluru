#!/usr/bin/env python3
"""
Simple HTTP server to serve the launcher interface
"""

import http.server
import socketserver
import json
import subprocess
import os
from urllib.parse import urlparse, parse_qs

class LauncherHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/start':
            self.handle_start()
        elif self.path == '/api/status':
            self.handle_status()
        else:
            self.send_error(404, "Not Found")
    
    def handle_start(self):
        """Handle application start request"""
        try:
            # Start the application
            result = subprocess.run(
                ["python", "launcher.py", "start"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                response_data = json.loads(result.stdout)
            else:
                response_data = {"success": False, "error": result.stderr}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
    
    def handle_status(self):
        """Handle status check request"""
        try:
            result = subprocess.run(
                ["python", "launcher.py", "status"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                response_data = json.loads(result.stdout)
            else:
                response_data = {"running": False}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"running": False, "error": str(e)}).encode())

def main():
    PORT = 8080
    
    print(f"🚀 Starting Launcher Server on port {PORT}")
    print(f"🌐 Open http://localhost:{PORT} in your browser")
    print("📝 Press Ctrl+C to stop")
    
    with socketserver.TCPServer(("", PORT), LauncherHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()
