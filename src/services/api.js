// API service for communicating with Express.js backend on Render
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://janata-audit-backend.onrender.com/api';

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
  }
  return await response.json();
};

// Submit feedback for a project
export const submitFeedback = async (projectId, feedback, rating, location, userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/submit-feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        projectId,
        feedback,
        rating: parseInt(rating),
        location,
        userId
      })
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Error submitting feedback:', error);
    throw error;
  }
};

// Submit a new project
export const submitProject = async (projectData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/submit-project`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(projectData)
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Error submitting project:', error);
    throw error;
  }
};

// Fetch all projects
export const fetchProjects = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/projects`);
    return await handleResponse(response);
  } catch (error) {
    console.error('Error fetching projects:', error);
    throw error;
  }
};

// Fetch a specific project by ID
export const fetchProject = async (projectId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}`);
    return await handleResponse(response);
  } catch (error) {
    console.error('Error fetching project:', error);
    throw error;
  }
};

// Fetch feedback for a specific project
export const fetchProjectFeedback = async (projectId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}/feedback`);
    return await handleResponse(response);
  } catch (error) {
    console.error('Error fetching project feedback:', error);
    throw error;
  }
};

// Trigger satellite analysis for a project
export const triggerSatelliteAnalysis = async (projectId, projectData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/trigger-satellite-analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        projectId,
        projectData
      })
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Error triggering satellite analysis:', error);
    throw error;
  }
};

// Get satellite analysis results
export const getSatelliteAnalysis = async (analysisId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/satellite-analysis/${analysisId}`);
    return await handleResponse(response);
  } catch (error) {
    console.error('Error fetching satellite analysis:', error);
    throw error;
  }
};

// Health check
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return await handleResponse(response);
  } catch (error) {
    console.error('Health check failed:', error);
    return { status: 'ERROR', error: error.message };
  }
};

// Utility function to get API base URL
export const getApiBaseUrl = () => API_BASE_URL;
