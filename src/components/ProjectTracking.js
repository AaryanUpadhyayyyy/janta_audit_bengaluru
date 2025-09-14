import React, { useState, useEffect, useCallback } from 'react';
import OpenStreetMapView from './OpenStreetMapView';
import EnhancedSatelliteAnalysis from './EnhancedSatelliteAnalysis';
import ProjectCard from './ProjectCard';
import FilterPanel from './FilterPanel';

const ProjectTracking = () => {
  const [projects, setProjects] = useState([]);
  const [filteredProjects, setFilteredProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [viewMode, setViewMode] = useState('map'); // 'map', 'list', 'analysis'
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    status: 'all',
    department: 'all',
    budgetRange: 'all',
    dateRange: 'all',
    searchQuery: ''
  });
  const [mapCenter, setMapCenter] = useState([12.9716, 77.5946]);
  const [mapZoom, setMapZoom] = useState(11);

  // Load projects on component mount
  useEffect(() => {
    loadProjects();
  }, []);

  // Filter projects when filters change
  useEffect(() => {
    filterProjects();
  }, [projects, filters]);

  const loadProjects = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('/api/projects');
      if (!response.ok) {
        throw new Error('Failed to load projects');
      }
      const data = await response.json();
      setProjects(data.projects || []);
    } catch (err) {
      setError(err.message);
      console.error('Error loading projects:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const filterProjects = () => {
    let filtered = [...projects];

    // Filter by status
    if (filters.status !== 'all') {
      filtered = filtered.filter(project => project.status === filters.status);
    }

    // Filter by department
    if (filters.department !== 'all') {
      filtered = filtered.filter(project => project.department === filters.department);
    }

    // Filter by budget range
    if (filters.budgetRange !== 'all') {
      const budgetRanges = {
        'low': [0, 1000000],      // 0-10 Lakh
        'medium': [1000000, 10000000], // 10 Lakh - 1 Crore
        'high': [10000000, 100000000], // 1-10 Crore
        'very-high': [100000000, Infinity] // 10+ Crore
      };
      const [min, max] = budgetRanges[filters.budgetRange];
      filtered = filtered.filter(project => {
        const budget = extractBudgetNumeric(project.budget);
        return budget >= min && budget <= max;
      });
    }

    // Filter by date range
    if (filters.dateRange !== 'all') {
      const now = new Date();
      const dateRanges = {
        'last-month': 30,
        'last-3-months': 90,
        'last-6-months': 180,
        'last-year': 365
      };
      const days = dateRanges[filters.dateRange];
      const cutoffDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
      
      filtered = filtered.filter(project => {
        const projectDate = new Date(project.startDate || project.timestamp);
        return projectDate >= cutoffDate;
      });
    }

    // Filter by search query
    if (filters.searchQuery) {
      const query = filters.searchQuery.toLowerCase();
      filtered = filtered.filter(project => 
        project.projectName?.toLowerCase().includes(query) ||
        project.description?.toLowerCase().includes(query) ||
        project.department?.toLowerCase().includes(query) ||
        project.contractorName?.toLowerCase().includes(query)
      );
    }

    setFilteredProjects(filtered);
  };

  const extractBudgetNumeric = (budgetStr) => {
    if (!budgetStr) return 0;
    
    const str = String(budgetStr).replace(/,/g, '').replace(/₹/g, '').replace(/Rs\./g, '');
    
    let multiplier = 1;
    if (str.includes('Lakh') || str.includes('L')) {
      multiplier = 100000;
    } else if (str.includes('Crore') || str.includes('Cr')) {
      multiplier = 10000000;
    }
    
    const numbers = str.match(/[\d.]+/);
    return numbers ? parseFloat(numbers[0]) * multiplier : 0;
  };

  const handleProjectSelect = (project) => {
    setSelectedProject(project);
    if (project.geoPoint) {
      setMapCenter([project.geoPoint.latitude, project.geoPoint.longitude]);
      setMapZoom(15);
    }
  };

  const handleLocationSelect = (location) => {
    // Find projects near the selected location
    const nearbyProjects = projects.filter(project => {
      if (!project.geoPoint) return false;
      
      const distance = calculateDistance(
        location.latitude, location.longitude,
        project.geoPoint.latitude, project.geoPoint.longitude
      );
      
      return distance < 1; // Within 1 km
    });
    
    if (nearbyProjects.length > 0) {
      setSelectedProject(nearbyProjects[0]);
    }
  };

  const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371; // Earth's radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  };

  const handleAnalysisComplete = (analysisData) => {
    if (selectedProject) {
      // Update project with analysis data
      setProjects(prevProjects => 
        prevProjects.map(project => 
          project.id === selectedProject.id 
            ? { ...project, satelliteAnalysis: analysisData }
            : project
        )
      );
    }
  };

  const getProjectMarkers = () => {
    return filteredProjects.map(project => ({
      lat: project.geoPoint?.latitude || 0,
      lng: project.geoPoint?.longitude || 0,
      name: project.projectName || 'Unknown Project',
      description: project.description || 'No description available',
      status: project.status,
      color: getStatusColor(project.status),
      radius: 500 // 500m radius
    })).filter(marker => marker.lat !== 0 && marker.lng !== 0);
  };

  const getStatusColor = (status) => {
    const colors = {
      'Completed': '#27ae60',
      'In Progress': '#3498db',
      'Pending': '#f39c12',
      'Cancelled': '#e74c3c',
      'Delayed': '#9b59b6'
    };
    return colors[status] || '#95a5a6';
  };

  const getProjectStats = () => {
    const stats = {
      total: filteredProjects.length,
      completed: filteredProjects.filter(p => p.status === 'Completed').length,
      inProgress: filteredProjects.filter(p => p.status === 'In Progress').length,
      pending: filteredProjects.filter(p => p.status === 'Pending').length,
      cancelled: filteredProjects.filter(p => p.status === 'Cancelled').length,
      totalBudget: filteredProjects.reduce((sum, p) => sum + extractBudgetNumeric(p.budget), 0)
    };
    return stats;
  };

  const stats = getProjectStats();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading projects...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <p className="font-bold">Error loading projects:</p>
        <p>{error}</p>
        <button 
          onClick={loadProjects}
          className="mt-2 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Header */}
      <div className="bg-white p-6 border-b">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold text-gray-800">Project Tracking</h1>
          <div className="flex space-x-2">
            <button
              onClick={() => setViewMode('map')}
              className={`px-4 py-2 rounded ${viewMode === 'map' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
            >
              Map View
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`px-4 py-2 rounded ${viewMode === 'list' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
            >
              List View
            </button>
            <button
              onClick={() => setViewMode('analysis')}
              className={`px-4 py-2 rounded ${viewMode === 'analysis' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
            >
              AI Analysis
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">{stats.total}</div>
            <div className="text-sm text-blue-800">Total Projects</div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{stats.completed}</div>
            <div className="text-sm text-green-800">Completed</div>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">{stats.inProgress}</div>
            <div className="text-sm text-yellow-800">In Progress</div>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-orange-600">{stats.pending}</div>
            <div className="text-sm text-orange-800">Pending</div>
          </div>
          <div className="bg-red-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-red-600">{stats.cancelled}</div>
            <div className="text-sm text-red-800">Cancelled</div>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-purple-600">
              ₹{(stats.totalBudget / 10000000).toFixed(1)}Cr
            </div>
            <div className="text-sm text-purple-800">Total Budget</div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Sidebar */}
        <div className="w-80 bg-gray-50 p-4 overflow-y-auto">
          <FilterPanel
            filters={filters}
            onFiltersChange={setFilters}
            projects={projects}
          />
          
          {viewMode === 'list' && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-4">Projects ({filteredProjects.length})</h3>
              <div className="space-y-4">
                {filteredProjects.map(project => (
                  <ProjectCard
                    key={project.id}
                    project={project}
                    isSelected={selectedProject?.id === project.id}
                    onClick={() => handleProjectSelect(project)}
                  />
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Main Content Area */}
        <div className="flex-1 p-4">
          {viewMode === 'map' && (
            <div className="h-full">
              <OpenStreetMapView
                center={mapCenter}
                zoom={mapZoom}
                onLocationSelect={handleLocationSelect}
                projectMarkers={getProjectMarkers()}
                analysisData={selectedProject?.satelliteAnalysis}
              />
            </div>
          )}

          {viewMode === 'analysis' && selectedProject && (
            <div className="h-full">
              <EnhancedSatelliteAnalysis
                projectId={selectedProject.id}
                projectData={selectedProject}
                onAnalysisComplete={handleAnalysisComplete}
              />
            </div>
          )}

          {viewMode === 'analysis' && !selectedProject && (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl mb-4">🤖</div>
                <h3 className="text-xl font-semibold text-gray-600 mb-2">
                  Select a Project for AI Analysis
                </h3>
                <p className="text-gray-500">
                  Choose a project from the list to perform satellite analysis
                </p>
              </div>
            </div>
          )}

          {viewMode === 'list' && (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl mb-4">📋</div>
                <h3 className="text-xl font-semibold text-gray-600 mb-2">
                  Project List View
                </h3>
                <p className="text-gray-500">
                  Use the sidebar to filter and select projects
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProjectTracking;
