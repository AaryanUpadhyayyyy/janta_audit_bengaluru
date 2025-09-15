// Data validation utility for Bengaluru projects
import { getAllProjects } from '../services/dataScraper';

// Validate project data structure
export const validateProjectData = () => {
  const { projects } = getAllProjects();
  const errors = [];
  const warnings = [];

  projects.forEach((project, index) => {
    // Required fields validation
    const requiredFields = ['id', 'projectName', 'status', 'department', 'wardNumber', 'budget', 'geoPoint'];
    
    requiredFields.forEach(field => {
      if (!project[field]) {
        errors.push(`Project ${index + 1} (${project.id}): Missing required field '${field}'`);
      }
    });

    // Data type validation
    if (project.geoPoint) {
      if (typeof project.geoPoint.latitude !== 'number' || typeof project.geoPoint.longitude !== 'number') {
        errors.push(`Project ${index + 1} (${project.id}): Invalid geoPoint coordinates`);
      }
      
      // Validate coordinates are within Bengaluru bounds
      if (project.geoPoint.latitude < 12.7 || project.geoPoint.latitude > 13.2 ||
          project.geoPoint.longitude < 77.3 || project.geoPoint.longitude > 77.8) {
        warnings.push(`Project ${index + 1} (${project.id}): Coordinates may be outside Bengaluru bounds`);
      }
    }

    // Status validation
    const validStatuses = ['Completed', 'In Progress', 'Pending', 'Cancelled'];
    if (!validStatuses.includes(project.status)) {
      errors.push(`Project ${index + 1} (${project.id}): Invalid status '${project.status}'`);
    }

    // Department validation
    const validDepartments = ['BBMP', 'BDA', 'BMRCL', 'BWSSB', 'BESCOM', 'PWD', 'Public Works Department', 'BBDA'];
    if (!validDepartments.includes(project.department)) {
      warnings.push(`Project ${index + 1} (${project.id}): Unknown department '${project.department}'`);
    }

    // Date validation
    if (project.startDate && project.endDate) {
      const startDate = new Date(project.startDate);
      const endDate = new Date(project.endDate);
      
      if (startDate > endDate) {
        errors.push(`Project ${index + 1} (${project.id}): Start date is after end date`);
      }
    }

    // Budget validation
    if (project.budget && !project.budget.includes('₹')) {
      warnings.push(`Project ${index + 1} (${project.id}): Budget format may be incorrect`);
    }

    // Progress validation
    if (project.progress !== undefined) {
      if (project.progress < 0 || project.progress > 100) {
        errors.push(`Project ${index + 1} (${project.id}): Progress must be between 0 and 100`);
      }
    }
  });

  return {
    isValid: errors.length === 0,
    errors,
    warnings,
    totalProjects: projects.length,
    projectsWithCoordinates: projects.filter(p => p.geoPoint?.latitude && p.geoPoint?.longitude).length
  };
};

// Get project statistics
export const getDetailedStatistics = () => {
  const { projects } = getAllProjects();
  
  const stats = {
    total: projects.length,
    byStatus: {},
    byDepartment: {},
    byWard: {},
    byRisk: {},
    budgetAnalysis: {
      total: 0,
      average: 0,
      min: Infinity,
      max: 0
    },
    timelineAnalysis: {
      completed: 0,
      overdue: 0,
      onTime: 0
    },
    geographicDistribution: {
      north: 0,
      south: 0,
      east: 0,
      west: 0,
      central: 0
    }
  };

  let totalBudget = 0;

  projects.forEach(project => {
    // Status count
    stats.byStatus[project.status] = (stats.byStatus[project.status] || 0) + 1;
    
    // Department count
    stats.byDepartment[project.department] = (stats.byDepartment[project.department] || 0) + 1;
    
    // Ward count
    stats.byWard[project.wardNumber] = (stats.byWard[project.wardNumber] || 0) + 1;
    
    // Risk count
    stats.byRisk[project.predictedDelayRisk] = (stats.byRisk[project.predictedDelayRisk] || 0) + 1;
    
    // Budget analysis
    if (project.budget) {
      const budget = parseFloat(project.budget.replace(/[^\d.]/g, '')) || 0;
      totalBudget += budget;
      stats.budgetAnalysis.min = Math.min(stats.budgetAnalysis.min, budget);
      stats.budgetAnalysis.max = Math.max(stats.budgetAnalysis.max, budget);
    }
    
    // Timeline analysis
    if (project.status === 'Completed' && project.actualCompletionDate) {
      stats.timelineAnalysis.completed++;
    } else if (project.status === 'In Progress' && project.endDate) {
      const endDate = new Date(project.endDate);
      const today = new Date();
      if (endDate < today) {
        stats.timelineAnalysis.overdue++;
      } else {
        stats.timelineAnalysis.onTime++;
      }
    }
    
    // Geographic distribution
    if (project.geoPoint) {
      const lat = project.geoPoint.latitude;
      const lng = project.geoPoint.longitude;
      
      if (lat > 12.9716) {
        if (lng > 77.5946) {
          stats.geographicDistribution.northeast++;
        } else {
          stats.geographicDistribution.northwest++;
        }
      } else {
        if (lng > 77.5946) {
          stats.geographicDistribution.southeast++;
        } else {
          stats.geographicDistribution.southwest++;
        }
      }
    }
  });

  stats.budgetAnalysis.total = totalBudget;
  stats.budgetAnalysis.average = totalBudget / projects.length;
  stats.budgetAnalysis.min = stats.budgetAnalysis.min === Infinity ? 0 : stats.budgetAnalysis.min;

  return stats;
};

// Validate map markers
export const validateMapMarkers = () => {
  const { projects } = getAllProjects();
  const markers = projects.map(project => ({
    lat: project.geoPoint?.latitude || 0,
    lng: project.geoPoint?.longitude || 0,
    name: project.projectName || 'Unknown Project',
    description: project.description || 'No description available',
    status: project.status,
    id: project.id
  })).filter(marker => marker.lat !== 0 && marker.lng !== 0);

  return {
    totalMarkers: markers.length,
    validMarkers: markers.filter(m => m.lat && m.lng && m.name && m.status).length,
    markersWithoutCoordinates: projects.length - markers.length,
    markers: markers
  };
};

export default {
  validateProjectData,
  getDetailedStatistics,
  validateMapMarkers
};
