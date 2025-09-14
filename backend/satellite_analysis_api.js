const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const router = express.Router();

// Enhanced Satellite Analysis API
router.post('/analyze-satellite', async (req, res) => {
  try {
    const { projectId, latitude, longitude, projectData } = req.body;

    if (!projectId || !latitude || !longitude) {
      return res.status(400).json({ error: 'Missing required parameters' });
    }

    // Prepare data for Python script
    const analysisData = {
      projectId,
      latitude: parseFloat(latitude),
      longitude: parseFloat(longitude),
      projectData: projectData || {}
    };

    // Run the enhanced satellite analyzer
    const pythonScript = path.join(__dirname, '../python_scripts/enhanced_satellite_analyzer.py');
    
    const pythonProcess = spawn('python', [pythonScript], {
      cwd: path.join(__dirname, '..'),
      env: {
        ...process.env,
        PROJECT_DATA: JSON.stringify(analysisData)
      }
    });

    let output = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error('Python script error:', errorOutput);
        return res.status(500).json({ 
          error: 'Analysis failed', 
          details: errorOutput 
        });
      }

      try {
        // Parse the output from Python script
        const result = JSON.parse(output);
        
        if (result.error) {
          return res.status(500).json({ error: result.error });
        }

        res.json({
          success: true,
          analysisReport: result.analysisReport || result,
          projectId: result.projectId
        });

      } catch (parseError) {
        console.error('Error parsing Python output:', parseError);
        console.error('Raw output:', output);
        res.status(500).json({ 
          error: 'Failed to parse analysis results',
          details: output
        });
      }
    });

    // Set timeout for the analysis
    setTimeout(() => {
      pythonProcess.kill();
      if (!res.headersSent) {
        res.status(408).json({ error: 'Analysis timeout' });
      }
    }, 300000); // 5 minutes timeout

  } catch (error) {
    console.error('Satellite analysis API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get analysis history for a project
router.get('/analysis-history/:projectId', async (req, res) => {
  try {
    const { projectId } = req.params;
    
    // This would typically query your database
    // For now, return a mock response
    res.json({
      success: true,
      analyses: []
    });

  } catch (error) {
    console.error('Error fetching analysis history:', error);
    res.status(500).json({ error: 'Failed to fetch analysis history' });
  }
});

// Get available free APIs status
router.get('/apis-status', (req, res) => {
  try {
    const apisStatus = {
      openstreetmap: {
        name: 'OpenStreetMap',
        status: 'active',
        description: 'Free mapping data and tiles',
        rateLimit: 'No official limit',
        usage: 'Mapping, geocoding, routing'
      },
      esri: {
        name: 'Esri World Imagery',
        status: 'active',
        description: 'Free satellite imagery tiles',
        rateLimit: 'No official limit',
        usage: 'Satellite imagery, aerial photography'
      },
      nominatim: {
        name: 'Nominatim',
        status: 'active',
        description: 'Free geocoding service',
        rateLimit: '1 request per second',
        usage: 'Address lookup, reverse geocoding'
      },
      cartodb: {
        name: 'CartoDB',
        status: 'active',
        description: 'Free map tiles',
        rateLimit: 'No official limit',
        usage: 'Alternative map styles'
      }
    };

    res.json({
      success: true,
      apis: apisStatus,
      lastUpdated: new Date().toISOString()
    });

  } catch (error) {
    console.error('Error fetching APIs status:', error);
    res.status(500).json({ error: 'Failed to fetch APIs status' });
  }
});

// Health check for satellite analysis service
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'satellite-analysis',
    timestamp: new Date().toISOString(),
    features: [
      'OpenStreetMap integration',
      'Free satellite imagery',
      'AI-powered analysis',
      'Time period detection',
      'Project status verification'
    ]
  });
});

module.exports = router;
