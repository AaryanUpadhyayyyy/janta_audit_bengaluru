const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');

// Get individual project details
router.get('/projects/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    // For now, return mock data - in production, this would fetch from Firestore
    const mockProject = {
      id: id,
      projectName: `Infrastructure Project ${id}`,
      description: 'A comprehensive infrastructure development project aimed at improving urban connectivity and public facilities in Bengaluru.',
      budget: 50000000,
      status: 'In Progress',
      location: 'Bengaluru, Karnataka',
      startDate: '2023-01-15',
      endDate: '2024-12-31',
      source: 'BBMP',
      department: 'BBMP',
      wardNumber: 15,
      contractor: 'ABC Construction Ltd.',
      geoPoint: {
        latitude: 12.9716 + (Math.random() - 0.5) * 0.1,
        longitude: 77.5946 + (Math.random() - 0.5) * 0.1
      },
      scrapedAt: new Date().toISOString(),
      sourceUrl: 'https://bbmp.gov.in/projects/' + id,
      aiAnalysis: {
        anomalies: [
          {
            type: 'Budget Anomaly',
            description: 'Project budget appears to be 15% higher than similar projects in the area',
            confidence: 85,
            severity: 'Medium'
          },
          {
            type: 'Timeline Risk',
            description: 'Project is 20% behind schedule based on current progress',
            confidence: 78,
            severity: 'High'
          }
        ],
        riskScore: 72,
        recommendations: [
          'Review budget allocation and cost estimates',
          'Implement accelerated construction schedule',
          'Increase monitoring frequency'
        ]
      },
      satelliteAnalysis: null // Will be populated when satellite analysis is run
    };

    res.json(mockProject);
  } catch (error) {
    console.error('Error fetching project details:', error);
    res.status(500).json({ error: 'Failed to fetch project details' });
  }
});

// Update project details
router.put('/projects/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;
    
    // In production, update Firestore document
    console.log(`Updating project ${id} with:`, updates);
    
    res.json({ 
      success: true, 
      message: 'Project updated successfully',
      projectId: id 
    });
  } catch (error) {
    console.error('Error updating project:', error);
    res.status(500).json({ error: 'Failed to update project' });
  }
});

// Get project documents
router.get('/projects/:id/documents', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Mock documents - in production, fetch from storage
    const documents = [
      {
        id: 'doc1',
        name: 'Project Proposal.pdf',
        type: 'PDF',
        size: '2.3 MB',
        uploadedAt: '2023-01-15T10:30:00Z',
        url: '/documents/project-proposal.pdf'
      },
      {
        id: 'doc2',
        name: 'Budget Allocation.xlsx',
        type: 'Excel',
        size: '156 KB',
        uploadedAt: '2023-01-20T14:15:00Z',
        url: '/documents/budget-allocation.xlsx'
      },
      {
        id: 'doc3',
        name: 'Progress Report Q1.pdf',
        type: 'PDF',
        size: '1.8 MB',
        uploadedAt: '2023-04-01T09:00:00Z',
        url: '/documents/progress-report-q1.pdf'
      }
    ];
    
    res.json(documents);
  } catch (error) {
    console.error('Error fetching project documents:', error);
    res.status(500).json({ error: 'Failed to fetch project documents' });
  }
});

// Upload project document
router.post('/projects/:id/documents', async (req, res) => {
  try {
    const { id } = req.params;
    const { name, type, size, url } = req.body;
    
    // In production, handle file upload to storage
    const document = {
      id: 'doc' + Date.now(),
      name,
      type,
      size,
      uploadedAt: new Date().toISOString(),
      url
    };
    
    res.json({ 
      success: true, 
      message: 'Document uploaded successfully',
      document 
    });
  } catch (error) {
    console.error('Error uploading document:', error);
    res.status(500).json({ error: 'Failed to upload document' });
  }
});

// Get project timeline/updates
router.get('/projects/:id/timeline', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Mock timeline data
    const timeline = [
      {
        id: 'update1',
        date: '2023-01-15T10:00:00Z',
        title: 'Project Initiated',
        description: 'Project officially started with ground-breaking ceremony',
        type: 'milestone',
        status: 'completed'
      },
      {
        id: 'update2',
        date: '2023-02-15T14:30:00Z',
        title: 'Foundation Work Completed',
        description: 'Foundation and basic structure work completed ahead of schedule',
        type: 'progress',
        status: 'completed'
      },
      {
        id: 'update3',
        date: '2023-03-20T11:15:00Z',
        title: 'Material Delivery Delayed',
        description: 'Concrete delivery delayed by 3 days due to transportation issues',
        type: 'issue',
        status: 'resolved'
      },
      {
        id: 'update4',
        date: '2023-04-10T16:45:00Z',
        title: 'Quality Inspection',
        description: 'Third-party quality inspection completed with satisfactory results',
        type: 'inspection',
        status: 'completed'
      },
      {
        id: 'update5',
        date: '2023-05-01T09:00:00Z',
        title: 'Current Progress',
        description: 'Project is 45% complete, slightly behind schedule',
        type: 'progress',
        status: 'ongoing'
      }
    ];
    
    res.json(timeline);
  } catch (error) {
    console.error('Error fetching project timeline:', error);
    res.status(500).json({ error: 'Failed to fetch project timeline' });
  }
});

// Add project update
router.post('/projects/:id/timeline', async (req, res) => {
  try {
    const { id } = req.params;
    const { title, description, type } = req.body;
    
    const update = {
      id: 'update' + Date.now(),
      date: new Date().toISOString(),
      title,
      description,
      type: type || 'update',
      status: 'ongoing'
    };
    
    // In production, save to Firestore
    console.log(`Adding timeline update for project ${id}:`, update);
    
    res.json({ 
      success: true, 
      message: 'Timeline update added successfully',
      update 
    });
  } catch (error) {
    console.error('Error adding timeline update:', error);
    res.status(500).json({ error: 'Failed to add timeline update' });
  }
});

// Get project analytics
router.get('/projects/:id/analytics', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Mock analytics data
    const analytics = {
      budgetUtilization: {
        allocated: 50000000,
        spent: 22500000,
        remaining: 27500000,
        percentage: 45
      },
      timelineProgress: {
        totalDays: 365,
        elapsedDays: 120,
        remainingDays: 245,
        percentage: 33
      },
      qualityMetrics: {
        inspectionsPassed: 8,
        inspectionsTotal: 10,
        qualityScore: 85
      },
      riskFactors: [
        {
          factor: 'Weather Delays',
          probability: 30,
          impact: 'Medium',
          mitigation: 'Indoor work scheduling'
        },
        {
          factor: 'Material Shortage',
          probability: 15,
          impact: 'High',
          mitigation: 'Alternative supplier contracts'
        }
      ]
    };
    
    res.json(analytics);
  } catch (error) {
    console.error('Error fetching project analytics:', error);
    res.status(500).json({ error: 'Failed to fetch project analytics' });
  }
});

module.exports = router;
