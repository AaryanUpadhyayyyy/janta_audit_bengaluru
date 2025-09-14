# Google Maps API Setup Guide

## 🗺️ How to Get a Google Maps API Key

### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click "Select a project" → "New Project"
4. Enter project name: "Janata Audit Bengaluru"
5. Click "Create"

### Step 2: Enable Required APIs
1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for and enable these APIs:
   - **Maps JavaScript API** (required for the map)
   - **Places API** (optional, for enhanced features)

### Step 3: Create API Key
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "API Key"
3. Copy the generated API key
4. (Optional) Click "Restrict Key" to add security restrictions

### Step 4: Add API Key to Your Project
1. Open `index.html` in your project
2. Find this line (around line 10):
   ```html
   <!-- <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY_HERE&libraries=places"></script> -->
   ```
3. Replace `YOUR_API_KEY_HERE` with your actual API key:
   ```html
   <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_ACTUAL_API_KEY&libraries=places"></script>
   ```
4. Remove the `<!--` and `-->` comment tags

### Step 5: Test Your Setup
1. Save the file
2. Open `index.html` in your browser
3. You should see the interactive map with project markers

## 🔒 Security Best Practices

### Restrict Your API Key (Recommended)
1. In Google Cloud Console, go to "APIs & Services" → "Credentials"
2. Click on your API key
3. Under "Application restrictions":
   - Choose "HTTP referrers (web sites)"
   - Add your domain (e.g., `localhost:8000/*`, `yourdomain.com/*`)
4. Under "API restrictions":
   - Choose "Restrict key"
   - Select only "Maps JavaScript API" and "Places API"

### Monitor Usage
1. Go to "APIs & Services" → "Dashboard"
2. Monitor your API usage and costs
3. Set up billing alerts if needed

## 💰 Pricing Information

Google Maps API has a free tier:
- **Maps JavaScript API**: 28,000 map loads per month (free)
- **Places API**: 1,000 requests per month (free)

For most development and small projects, the free tier is sufficient.

## 🚨 Common Issues

### "InvalidKeyMapError"
- Check that your API key is correct
- Ensure the Maps JavaScript API is enabled
- Verify there are no extra spaces in the API key

### "RefererNotAllowedMapError"
- Add your domain to the HTTP referrers list in API key restrictions
- For local development, add `localhost:8000/*`

### Map Not Loading
- Check browser console for error messages
- Verify the API key is properly placed in the HTML
- Ensure you have an active internet connection

## 🔧 Alternative: Use Without API Key

If you don't want to set up Google Maps API right now, the application will still work! It will show a helpful message in place of the map, and you can still:

- View all projects in the list
- Filter projects by ward, department, and status
- See project details
- Use all other features

The map is just one feature - the core functionality works without it.

## 📞 Need Help?

- [Google Maps JavaScript API Documentation](https://developers.google.com/maps/documentation/javascript)
- [Google Cloud Console Help](https://cloud.google.com/docs)
- [API Key Best Practices](https://developers.google.com/maps/api-key-best-practices)
