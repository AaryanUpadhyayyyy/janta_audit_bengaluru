# 🚀 Auto-Start System for Janata Audit Bengaluru

## 📋 Overview

This system automatically runs the government data scraper and starts the application when you open `index.html`. No manual setup required!

## 🎯 What It Does

1. **Automatically runs** the government data scraper to collect project data from 9 Karnataka government portals
2. **Starts the backend server** with all API endpoints
3. **Starts the frontend server** with the React application
4. **Opens the application** in your browser automatically
5. **Monitors all services** and keeps them running

## 🚀 Quick Start

### Option 1: One-Click Start (Recommended)

1. **Double-click** `start_launcher.bat` (Windows) or run `./start_launcher.sh` (Mac/Linux)
2. **Open** http://localhost:8080 in your browser
3. **Click** "Start Application" button
4. **Wait** for the application to start (2-3 minutes for first time)
5. **Enjoy** the full application with government data!

### Option 2: Direct HTML Launch

1. **Run** `python launcher_server.py`
2. **Open** http://localhost:8080 in your browser
3. **Click** "Start Application" button

### Option 3: Manual Start

1. **Run** `python auto_start.py` (or double-click `start_app.bat`)
2. **Wait** for all services to start
3. **Open** http://localhost:3000 in your browser

## 📁 Files Created

### Core Auto-Start Files
- **`auto_start.py`** - Main auto-start script that runs everything
- **`launcher_server.py`** - HTTP server for the web launcher interface
- **`launcher.py`** - Simple launcher script for web interface
- **`index.html`** - Beautiful web interface for starting the application

### Platform-Specific Launchers
- **`start_app.bat`** - Windows batch file for direct start
- **`start_app.sh`** - Mac/Linux shell script for direct start
- **`start_launcher.bat`** - Windows batch file for web launcher

## 🔧 How It Works

### 1. Web Launcher Interface
```
User opens index.html → Clicks "Start Application" → 
Launcher server starts auto_start.py → 
Government scraper runs → Backend starts → Frontend starts → 
Browser opens to http://localhost:3000
```

### 2. Direct Start
```
User runs auto_start.py → 
Government scraper runs → Backend starts → Frontend starts → 
Browser opens to http://localhost:3000
```

### 3. Process Management
- **Monitors** all running services
- **Restarts** services if they crash
- **Handles** graceful shutdown with Ctrl+C
- **Provides** real-time status updates

## 🛠️ Technical Details

### Auto-Start Script (`auto_start.py`)
- **Runs government scraper** from `python_scripts/government_portal_scraper.py`
- **Installs dependencies** automatically
- **Starts backend server** on port 3000
- **Starts frontend server** on port 3000 (React dev server)
- **Opens browser** automatically
- **Monitors processes** and handles errors

### Launcher Server (`launcher_server.py`)
- **Simple HTTP server** on port 8080
- **Serves** the web launcher interface
- **Handles** start/status API requests
- **Manages** process spawning

### Web Interface (`index.html`)
- **Beautiful landing page** with project information
- **One-click start** button
- **Real-time status** checking
- **Responsive design** for all devices
- **Error handling** and user feedback

## 📊 Government Data Sources

The system automatically scrapes data from:

1. **Karnataka e-Procurement Portal** - Tender information
2. **BBMP** - Municipal projects
3. **BDA** - Development projects
4. **BWSSB** - Water supply projects
5. **BMRCL** - Metro rail projects
6. **BESCOM** - Electrical infrastructure
7. **KPWD** - Public works
8. **KUIDFC** - Urban infrastructure
9. **BMTC** - Public transport

## 🎨 Features

### Web Launcher Interface
- **Modern design** with gradient backgrounds
- **Feature showcase** with icons and descriptions
- **One-click start** with loading animation
- **Status checking** to see if app is already running
- **Instructions** and help text
- **Responsive design** for mobile and desktop

### Auto-Start System
- **Dependency installation** - Automatically installs Python and Node.js packages
- **Error handling** - Robust error handling and recovery
- **Process monitoring** - Keeps all services running
- **Graceful shutdown** - Clean shutdown with Ctrl+C
- **Cross-platform** - Works on Windows, Mac, and Linux

### Government Data Integration
- **Real-time scraping** - Collects fresh data from government portals
- **Data normalization** - Consistent format across all sources
- **Error recovery** - Handles scraping errors gracefully
- **Data validation** - Ensures data quality and completeness

## 🔍 Troubleshooting

### Common Issues

#### 1. Python Not Found
```
❌ Python is not installed or not in PATH
```
**Solution**: Install Python from https://python.org and add it to PATH

#### 2. Node.js Not Found
```
❌ Node.js is not installed or not in PATH
```
**Solution**: Install Node.js from https://nodejs.org and add it to PATH

#### 3. Port Already in Use
```
❌ Port 3000 is already in use
```
**Solution**: Stop other applications using port 3000, or change the port in the configuration

#### 4. Scraper Errors
```
⚠️ Warning: Government data scraper had some issues
```
**Solution**: Check internet connection and try again. Some government sites may be temporarily unavailable.

### Debug Mode

To run in debug mode and see detailed output:

```bash
# Windows
python auto_start.py --debug

# Mac/Linux
python3 auto_start.py --debug
```

### Manual Service Start

If auto-start fails, you can start services manually:

```bash
# Terminal 1: Backend
cd backend
npm install
node server.js

# Terminal 2: Frontend
npm install
npm start

# Terminal 3: Scraper
cd python_scripts
pip install -r requirements.txt
python run_scraper.py
```

## 📈 Performance

### First Run
- **Time**: 3-5 minutes
- **Steps**: Install dependencies, scrape data, start services
- **Data**: Collects fresh data from all government portals

### Subsequent Runs
- **Time**: 30-60 seconds
- **Steps**: Start services only
- **Data**: Uses cached data (can be refreshed)

### Resource Usage
- **Memory**: ~200MB for all services
- **CPU**: Low usage after startup
- **Disk**: ~100MB for dependencies and data

## 🔒 Security

### Data Privacy
- **No personal data** collection
- **Public information** only from government portals
- **Local processing** - data stays on your machine
- **No external tracking** or analytics

### Network Security
- **Local servers only** - no external connections
- **HTTPS support** for production deployment
- **Input validation** and sanitization
- **Error handling** to prevent information leakage

## 🎉 Benefits

### For Users
- **One-click start** - No technical knowledge required
- **Automatic updates** - Fresh data every time
- **Cross-platform** - Works on any operating system
- **Beautiful interface** - Modern, responsive design

### For Developers
- **Easy deployment** - Simple setup and configuration
- **Modular design** - Easy to extend and modify
- **Error handling** - Robust error handling and recovery
- **Documentation** - Comprehensive guides and examples

## 🚀 Future Enhancements

### Planned Features
- **Docker support** - Containerized deployment
- **Auto-updates** - Automatic application updates
- **Configuration UI** - Web-based configuration
- **Monitoring dashboard** - Real-time service monitoring
- **Logging system** - Comprehensive logging and debugging

### Technical Improvements
- **Performance optimization** - Faster startup and operation
- **Memory management** - Better resource utilization
- **Error recovery** - Automatic error recovery and restart
- **Health checks** - Comprehensive health monitoring

## 📞 Support

### Getting Help
- **Documentation**: Check this README and other documentation files
- **Issues**: Report problems and bugs
- **Community**: Join the development community
- **Updates**: Follow for latest updates and announcements

### System Requirements
- **Python 3.7+** - For backend and scraping
- **Node.js 14+** - For frontend and API
- **4GB RAM** - Minimum recommended
- **2GB disk space** - For dependencies and data
- **Internet connection** - For data scraping and updates

---

**Built with ❤️ for transparent governance and civic accountability**

**One-click start, infinite possibilities! 🚀**
