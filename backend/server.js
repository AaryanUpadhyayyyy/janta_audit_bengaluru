const express = require('express');
const cors = require('cors');
const admin = require('firebase-admin');
const path = require('path');
const satelliteAnalysisRouter = require('./satellite_analysis_api');
const projectDetailsRouter = require('./project_details_api');
const healthEngineRouter = require('./routes/healthEngineRouter');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize Firebase Admin
let serviceAccount;
try {
  // Try to get service account from environment variable (for Render)
  if (process.env.FIREBASE_SERVICE_ACCOUNT_KEY) {
    serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT_KEY);
  } else {
    // Fallback to local file (for development)
    serviceAccount = require('./serviceAccountKey.json');
  }
} catch (error) {
  console.error('Error loading Firebase service account:', error);
  console.log('Please set FIREBASE_SERVICE_ACCOUNT_KEY environment variable or add serviceAccountKey.json file');
}

let db;
if (serviceAccount) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: process.env.FIREBASE_DATABASE_URL || "https://jannat-audit.firebaseio.com"
  });
  db = admin.firestore();
  console.log('🔥 Firebase Admin initialized successfully');
} else {
  console.warn('Firebase Admin not initialized - API will not work without proper configuration');
}

// API Routes

// Satellite Analysis API
app.use('/api', satelliteAnalysisRouter);
app.use('/api', projectDetailsRouter);
app.use('/api', healthEngineRouter);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development',
    firebase: !!admin.apps.length
  });
});

// Submit feedback endpoint
app.post('/api/submit-feedback', async (req, res) => {
  try {
    const { projectId, feedback, rating, location, userId } = req.body;
    
    // Validate input
    if (!projectId || !feedback || !rating) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    if (!db) {
      return res.status(500).json({ error: 'Database not initialized' });
    }
    
    // Save to Firestore
    const feedbackData = {
      projectId,
      feedback,
      rating: parseInt(rating),
      location: location || null,
      userId: userId || 'anonymous',
      timestamp: admin.firestore.FieldValue.serverTimestamp(),
      status: 'pending'
    };
    
    const docRef = await db.collection('userFeedback').add(feedbackData);
    
    res.json({ 
      success: true, 
      feedbackId: docRef.id,
      message: 'Feedback submitted successfully' 
    });
    
  } catch (error) {
    console.error('Error submitting feedback:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Submit project endpoint
app.post('/api/submit-project', async (req, res) => {
  try {
    const projectData = req.body;
    
    // Validate required fields
    const requiredFields = ['projectName', 'description', 'location', 'budget'];
    for (const field of requiredFields) {
      if (!projectData[field]) {
        return res.status(400).json({ error: `Missing required field: ${field}` });
      }
    }
    
    if (!db) {
      return res.status(500).json({ error: 'Database not initialized' });
    }
    
    // Add metadata
    const project = {
      ...projectData,
      status: 'pending',
      submittedBy: projectData.userId || 'anonymous',
      timestamp: admin.firestore.FieldValue.serverTimestamp(),
      upvotes: 0,
      downvotes: 0
    };
    
    // Save to Firestore
    const docRef = await db.collection('projects').add(project);
    
    res.json({ 
      success: true, 
      projectId: docRef.id,
      message: 'Project submitted successfully' 
    });
    
  } catch (error) {
    console.error('Error submitting project:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get projects endpoint
app.get('/api/projects', async (req, res) => {
  try {
    if (!db) {
      return res.status(500).json({ error: 'Database not initialized' });
    }
    
    const snapshot = await db.collection('projects')
      .orderBy('timestamp', 'desc')
      .limit(50)
      .get();
    
    const projects = [];
    snapshot.forEach(doc => {
      projects.push({
        id: doc.id,
        ...doc.data()
      });
    });
    
    res.json({ projects });
    
  } catch (error) {
    console.error('Error fetching projects:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get project by ID endpoint
app.get('/api/projects/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    if (!db) {
      return res.status(500).json({ error: 'Database not initialized' });
    }
    
    const doc = await db.collection('projects').doc(id).get();
    
    if (!doc.exists) {
      return res.status(404).json({ error: 'Project not found' });
    }
    
    res.json({
      id: doc.id,
      ...doc.data()
    });
    
  } catch (error) {
    console.error('Error fetching project:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get feedback for a project
app.get('/api/projects/:id/feedback', async (req, res) => {
  try {
    const { id } = req.params;
    
    if (!db) {
      return res.status(500).json({ error: 'Database not initialized' });
    }
    
    const snapshot = await db.collection('userFeedback')
      .where('projectId', '==', id)
      .orderBy('timestamp', 'desc')
      .get();
    
    const feedback = [];
    snapshot.forEach(doc => {
      feedback.push({
        id: doc.id,
        ...doc.data()
      });
    });
    
    res.json({ feedback });
    
  } catch (error) {
    console.error('Error fetching feedback:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Satellite Inspector endpoints (simplified for Express.js)
app.post('/api/trigger-satellite-analysis', async (req, res) => {
  try {
    const { projectId, projectData } = req.body;
    
    if (!projectId || !projectData) {
      return res.status(400).json({ error: 'Missing projectId or projectData' });
    }
    
    // For now, return a mock response
    // In production, you would trigger the Python satellite analysis script
    res.json({
      success: true,
      message: 'Satellite analysis triggered',
      analysisId: `analysis_${Date.now()}`,
      status: 'processing'
    });
    
  } catch (error) {
    console.error('Error triggering satellite analysis:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/api/satellite-analysis/:analysisId', async (req, res) => {
  try {
    const { analysisId } = req.params;
    
    // Mock satellite analysis results
    res.json({
      analysisId,
      status: 'completed',
      results: {
        ndbiChange: 0.15,
        structureDetected: true,
        progressPercentage: 75,
        redFlags: [],
        confidence: 0.85,
        lastUpdated: new Date().toISOString()
      }
    });
    
  } catch (error) {
    console.error('Error fetching satellite analysis:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Serve static files (if hosting React build)
app.use(express.static(path.join(__dirname, '../build')));

// Catch all handler for React Router
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../build/index.html'));
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔥 Firebase: ${admin.apps.length ? 'Connected' : 'Not connected'}`);
});
