# 🛰️ Satellite Inspector - Advanced AI Module

The Satellite Inspector is an advanced AI module that provides unbiased, physical proof of on-ground project progress by analyzing satellite imagery over time. This powerful tool verifies claims made by contractors and government agencies using Google Earth Engine.

## 🎯 Overview

The Satellite Inspector automatically analyzes satellite imagery to detect physical changes in project areas, providing objective verification of project progress claims. It uses the Normalized Difference Built-up Index (NDBI) to measure the presence of built-up structures like concrete, asphalt, and buildings.

## 🏗️ Architecture

### Core Components

1. **satellite_inspector.py** - Main Python module with Google Earth Engine integration
2. **satelliteInspector.ts** - Firebase Cloud Function with Firestore triggers
3. **SatelliteAnalysis.js** - React component for displaying analysis results
4. **gee_setup.py** - Setup and configuration script

### Data Flow

```
Project Created/Updated → Firestore Trigger → Cloud Function → Python Script → Google Earth Engine → Analysis Results → Firestore → Frontend Display
```

## 🔧 Technical Implementation

### Google Earth Engine Integration

- **Data Source**: Sentinel-2 satellite imagery
- **Analysis Method**: NDBI (Normalized Difference Built-up Index)
- **Formula**: `NDBI = (SWIR - NIR) / (SWIR + NIR)`
- **Bands Used**: B11 (SWIR1) and B8 (NIR)
- **Resolution**: 10m per pixel
- **Cloud Filtering**: < 20% cloud cover

### Time Period Analysis

- **Before Period**: 6-9 months before project start
- **After Period**: Most recent 1-2 months
- **ROI Size**: 500m radius around project location
- **Image Selection**: Least cloud cover for each period

### Change Detection Algorithm

1. **Image Acquisition**: Query Sentinel-2 collection for both time periods
2. **NDBI Calculation**: Compute NDBI for each image
3. **Mean Value Calculation**: Calculate mean NDBI within ROI
4. **Change Analysis**: Compare before/after values
5. **Mismatch Detection**: Compare with expected changes based on project status

## 📊 Analysis Results

### Metrics Provided

- **NDBI Change Percentage**: Physical change in built-up structures
- **Before/After Mean NDBI**: Raw values for each time period
- **Project Duration**: Time since project start
- **Confidence Level**: Analysis reliability (high/medium/low)
- **Mismatch Detection**: Whether claims match physical evidence

### Red Flag Generation

The system creates red flags when:
- Project status is "In Progress" but shows minimal physical change
- Project has been ongoing for 6+ months with < 5% NDBI change
- Unexpectedly high changes for "Pending" projects
- Significant mismatches between claims and satellite evidence

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
cd python_scripts
pip install -r requirements.txt
```

### 2. Google Earth Engine Setup

```bash
# Run the setup script
python gee_setup.py

# Or manually authenticate
earthengine authenticate
```

### 3. Service Account Setup (Production)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select a project
3. Enable Earth Engine API
4. Create service account with Earth Engine access
5. Download JSON key file as `serviceAccountKey.json`
6. Place in `python_scripts/` directory

### 4. Deploy Cloud Functions

```bash
# Deploy all functions including satellite inspector
firebase deploy --only functions
```

## 🔄 Usage

### Automatic Triggers

The satellite analysis runs automatically when:
- A new project is created in Firestore
- A project's status field is updated
- Manual trigger via Cloud Function

### Manual Triggers

```javascript
// From frontend
const triggerSatelliteAnalysis = httpsCallable(functions, 'triggerSatelliteAnalysis');
await triggerSatelliteAnalysis({ projectId: 'project-id' });
```

### Viewing Results

Satellite analysis results are displayed in the project detail page with:
- NDBI change percentage
- Analysis confidence level
- Mismatch alerts
- Technical details
- Time period information

## 📈 Analysis Logic

### Expected Changes by Status

| Project Status | Min NDBI Change | Max NDBI Change | Notes |
|----------------|-----------------|-----------------|-------|
| Pending | 0% | 5% | Minimal expected change |
| In Progress | 5% | 50% | Significant change expected |
| Completed | 10% | 100% | Major change expected |
| Cancelled | 0% | 10% | Limited change expected |

### Severity Levels

- **High**: Project ongoing 6+ months with < 5% change
- **Medium**: Status/change mismatch or unexpected high change
- **Low**: Minor discrepancies or new projects

## 🔍 Technical Details

### NDBI Calculation

```python
# For Sentinel-2 imagery
nir = image.select('B8')      # Near Infrared
swir1 = image.select('B11')   # Short Wave Infrared 1
ndbi = swir1.subtract(nir).divide(swir1.add(nir))
```

### ROI Definition

```python
# 500m buffer around project location
point = ee.Geometry.Point([longitude, latitude])
roi = point.buffer(500)  # 500 meters
```

### Image Filtering

```python
collection = (ee.ImageCollection('COPERNICUS/S2_SR')
             .filterBounds(roi)
             .filterDate(start_date, end_date)
             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)))
```

## 🛠️ Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure Google Earth Engine account is set up
   - Check service account permissions
   - Verify API keys are correct

2. **No Images Found**
   - Check if project location is valid
   - Verify time periods have available imagery
   - Consider adjusting cloud cover threshold

3. **Analysis Failures**
   - Check project has valid geoPoint data
   - Ensure sufficient time has passed for analysis
   - Verify Google Earth Engine quotas

### Debugging

```bash
# Test satellite inspector locally
cd python_scripts
python satellite_inspector.py

# Check Cloud Function logs
firebase functions:log --only satelliteInspector

# View analysis results in Firestore
# Check 'projects/{projectId}/satelliteAnalysis' field
```

## 📊 Performance Considerations

### Processing Time
- **Typical Analysis**: 2-5 minutes per project
- **Timeout**: 10 minutes maximum
- **Concurrent Limits**: 1 analysis per project at a time

### Data Storage
- **Analysis Results**: Stored in project document
- **Red Flags**: Stored in aiRedFlags collection
- **Logs**: Stored in satelliteAnalysisLogs collection

### Cost Optimization
- **Image Caching**: Reuse images when possible
- **ROI Optimization**: Use appropriate buffer sizes
- **Batch Processing**: Process multiple projects efficiently

## 🔮 Future Enhancements

### Planned Features
- **Multi-temporal Analysis**: Track changes over multiple time periods
- **Advanced Indices**: NDVI, NDWI, and other spectral indices
- **Machine Learning**: AI-powered change detection
- **Real-time Monitoring**: Continuous satellite monitoring
- **Historical Analysis**: Long-term trend analysis

### Integration Opportunities
- **Weather Data**: Correlate with weather patterns
- **Traffic Data**: Analyze traffic flow changes
- **Population Data**: Demographic impact analysis
- **Environmental Data**: Ecological impact assessment

## 📚 References

- [Google Earth Engine Documentation](https://developers.google.com/earth-engine)
- [Sentinel-2 Data Description](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR)
- [NDBI Index Information](https://www.usgs.gov/land-resources/nli/landsat/normalized-difference-built-up-index)
- [Firebase Cloud Functions](https://firebase.google.com/docs/functions)

---

**The Satellite Inspector** - Providing objective, satellite-based verification for civic accountability in Bengaluru.
