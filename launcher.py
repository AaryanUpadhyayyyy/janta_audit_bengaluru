#!/usr/bin/env python3
"""
Simple launcher script that can be called from the web interface
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def start_application():
    """Start the application and return status"""
    try:
        # Check if we're in the right directory
        if not Path("auto_start.py").exists():
            return {"success": False, "error": "Auto-start script not found"}
        
        # Start the auto-start script in the background
        if os.name == 'nt':  # Windows
            process = subprocess.Popen(
                ["python", "auto_start.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:  # Unix-like
            process = subprocess.Popen(
                ["python3", "auto_start.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
        
        return {"success": True, "pid": process.pid, "message": "Application starting..."}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_status():
    """Check if the application is running"""
    try:
        import requests
        response = requests.get("http://localhost:3000/api/health", timeout=5)
        return {"running": response.status_code == 200}
    except:
        return {"running": False}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            result = start_application()
            print(json.dumps(result))
        elif command == "status":
            result = check_status()
            print(json.dumps(result))
        else:
            print(json.dumps({"success": False, "error": "Unknown command"}))
    else:
        print(json.dumps({"success": False, "error": "No command provided"}))
