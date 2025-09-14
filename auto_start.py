#!/usr/bin/env python3
"""
Auto-start script for Janata Audit Bengaluru
Automatically runs government data scraper and starts the application
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return the process"""
    try:
        print(f"🚀 Running: {command}")
        process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"❌ Error running command '{command}': {e}")
        return None

def run_scraper():
    """Run the government data scraper"""
    print("📊 Starting Government Data Scraper...")
    print("=" * 50)
    
    scraper_path = Path("python_scripts")
    if not scraper_path.exists():
        print("❌ Python scripts directory not found!")
        return False
    
    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    install_process = run_command("pip install -r requirements.txt", cwd=scraper_path)
    if install_process:
        install_process.wait()
        if install_process.returncode != 0:
            print("⚠️  Warning: Some Python dependencies may not have installed correctly")
    
    # Run the scraper
    print("🕷️  Running government portal scraper...")
    scraper_process = run_command("python run_scraper.py", cwd=scraper_path)
    if scraper_process:
        scraper_process.wait()
        if scraper_process.returncode == 0:
            print("✅ Government data scraper completed successfully!")
        else:
            print("⚠️  Warning: Government data scraper had some issues")
    else:
        print("❌ Failed to start government data scraper")
        return False
    
    return True

def start_backend():
    """Start the backend server"""
    print("🔧 Starting Backend Server...")
    
    backend_path = Path("backend")
    if not backend_path.exists():
        print("❌ Backend directory not found!")
        return None
    
    # Install Node.js dependencies
    print("📦 Installing Node.js dependencies...")
    install_process = run_command("npm install", cwd=backend_path)
    if install_process:
        install_process.wait()
        if install_process.returncode != 0:
            print("⚠️  Warning: Some Node.js dependencies may not have installed correctly")
    
    # Start the backend server
    print("🚀 Starting backend server...")
    backend_process = run_command("node server.js", cwd=backend_path)
    if backend_process:
        print("✅ Backend server started!")
        return backend_process
    else:
        print("❌ Failed to start backend server")
        return None

def start_frontend():
    """Start the frontend development server"""
    print("🎨 Starting Frontend Server...")
    
    # Install Node.js dependencies
    print("📦 Installing frontend dependencies...")
    install_process = run_command("npm install")
    if install_process:
        install_process.wait()
        if install_process.returncode != 0:
            print("⚠️  Warning: Some frontend dependencies may not have installed correctly")
    
    # Start the frontend server
    print("🚀 Starting frontend server...")
    frontend_process = run_command("npm start")
    if frontend_process:
        print("✅ Frontend server started!")
        return frontend_process
    else:
        print("❌ Failed to start frontend server")
        return None

def open_browser():
    """Open the application in the browser"""
    print("🌐 Opening application in browser...")
    time.sleep(5)  # Wait for servers to start
    try:
        webbrowser.open("http://localhost:3000")
        print("✅ Application opened in browser!")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("🌐 Please open http://localhost:3000 in your browser")

def main():
    """Main function to start everything"""
    print("🚀 Janata Audit Bengaluru - Auto Start")
    print("=" * 50)
    print("This will automatically:")
    print("1. Run the government data scraper")
    print("2. Start the backend server")
    print("3. Start the frontend server")
    print("4. Open the application in your browser")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("package.json").exists():
        print("❌ Please run this script from the project root directory")
        return 1
    
    processes = []
    
    try:
        # Step 1: Run the scraper
        print("\n📊 Step 1: Running Government Data Scraper")
        scraper_success = run_scraper()
        if not scraper_success:
            print("⚠️  Continuing despite scraper issues...")
        
        # Step 2: Start backend server
        print("\n🔧 Step 2: Starting Backend Server")
        backend_process = start_backend()
        if backend_process:
            processes.append(("Backend", backend_process))
        else:
            print("❌ Failed to start backend server")
            return 1
        
        # Step 3: Start frontend server
        print("\n🎨 Step 3: Starting Frontend Server")
        frontend_process = start_frontend()
        if frontend_process:
            processes.append(("Frontend", frontend_process))
        else:
            print("❌ Failed to start frontend server")
            return 1
        
        # Step 4: Open browser
        print("\n🌐 Step 4: Opening Application")
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Step 5: Keep everything running
        print("\n✅ All services started successfully!")
        print("🌐 Application is available at: http://localhost:3000")
        print("🔧 Backend API is available at: http://localhost:3000/api")
        print("\n📝 Press Ctrl+C to stop all services")
        print("=" * 50)
        
        # Monitor processes
        while True:
            time.sleep(1)
            for name, process in processes:
                if process.poll() is not None:
                    print(f"❌ {name} server stopped unexpectedly!")
                    return 1
    
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all services...")
        for name, process in processes:
            print(f"🛑 Stopping {name} server...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("✅ All services stopped!")
        return 0
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
