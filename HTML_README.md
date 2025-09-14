# Janata Audit Bengaluru - HTML Version

A simplified HTML/CSS/JavaScript version of the Janata Audit Bengaluru civic accountability platform.

## 🚀 Quick Start

1. **Open the application:**
   ```bash
   # Simply open index.html in your web browser
   start index.html
   ```

2. **Or serve it locally:**
   ```bash
   # Using Python (if installed)
   python -m http.server 8000
   
   # Using Node.js (if installed)
   npx serve .
   
   # Then visit http://localhost:8000
   ```

## 📁 Files Structure

```
├── index.html          # Main HTML file
├── styles.css          # CSS styling
├── script.js           # JavaScript functionality
└── HTML_README.md      # This file
```

## ✨ Features

### ✅ Working Features
- **Interactive Map**: Google Maps integration (requires API key)
- **Project Tracking**: View projects with status indicators
- **Filtering**: Filter projects by ward, department, and status
- **Responsive Design**: Works on desktop and mobile
- **Project Details**: Detailed project information modal
- **User Authentication**: Simulated login system
- **Modern UI**: Clean, professional design

### 🔧 Configuration Required

1. **Google Maps API Key (Optional):**
   - The application works without a Google Maps API key
   - Without the API key, you'll see a helpful message instead of the map
   - To enable the interactive map, follow the guide in `GOOGLE_MAPS_SETUP.md`
   - Or simply uncomment and add your API key in `index.html`:
     ```html
     <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY_HERE&libraries=places"></script>
     ```

2. **Backend Integration (Optional):**
   - The current version uses sample data
   - To connect to the Express.js backend, update the API endpoints in `script.js`

## 🎯 Sample Data

The application includes 5 sample projects:
- Road Widening - MG Road (In Progress)
- Metro Station Construction (Completed)
- Water Pipeline Installation (Pending)
- Park Development (In Progress)
- Street Lighting Upgrade (Completed)

## 🎨 Customization

### Adding New Projects
Edit the `sampleProjects` array in `script.js`:

```javascript
const sampleProjects = [
    {
        id: 6,
        projectName: "Your Project Name",
        description: "Project description",
        wardNumber: "Ward 5",
        department: "BBMP",
        status: "In Progress",
        budget: "₹1,00,00,000",
        location: { lat: 12.9716, lng: 77.5946 },
        startDate: "2024-01-01",
        endDate: "2024-12-31",
        predictedDelayRisk: "Medium"
    }
];
```

### Styling
- Modify `styles.css` to change colors, fonts, and layout
- The design uses CSS Grid and Flexbox for responsive layouts
- Color scheme: Blue (#2563eb) primary, with status-based colors

### Functionality
- Add new features in `script.js`
- The code is well-commented and modular
- Easy to extend with additional functionality

## 🔗 Backend Integration

To connect with the Express.js backend:

1. **Update API endpoints** in `script.js`:
   ```javascript
   const API_BASE_URL = 'http://localhost:3000/api';
   ```

2. **Replace sample data** with real API calls:
   ```javascript
   async function fetchProjects() {
       const response = await fetch(`${API_BASE_URL}/projects`);
       return await response.json();
   }
   ```

## 📱 Mobile Support

The application is fully responsive and includes:
- Mobile-friendly navigation
- Touch-optimized map interactions
- Responsive project cards
- Mobile-specific layouts

## 🚀 Deployment

### Static Hosting
Deploy to any static hosting service:
- **Netlify**: Drag and drop the files
- **Vercel**: Connect your GitHub repository
- **GitHub Pages**: Push to a GitHub repository
- **Firebase Hosting**: Use Firebase CLI

### Local Development
```bash
# Serve locally
python -m http.server 8000
# or
npx serve .
```

## 🔧 Troubleshooting

### Google Maps Not Loading
- Ensure you have a valid Google Maps API key
- Check that the Maps JavaScript API is enabled
- Verify the API key is correctly placed in `index.html`

### Styling Issues
- Clear browser cache
- Check browser console for CSS errors
- Ensure all CSS files are loading correctly

### JavaScript Errors
- Open browser developer tools (F12)
- Check the Console tab for error messages
- Ensure all JavaScript files are loading

## 📄 License

This project is part of the Janata Audit Bengaluru platform.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Janata Audit Bengaluru** - Empowering citizens through transparency and accountability.
