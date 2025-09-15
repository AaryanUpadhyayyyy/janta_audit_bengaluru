import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useProjects } from '../contexts/ProjectContext';
import OpenStreetMapView from '../components/OpenStreetMapView';
import FilterPanel from '../components/FilterPanel';
import ProjectCard from '../components/ProjectCard';
import { MapPin, Filter, Users, Brain, ArrowRight } from 'lucide-react';

const HomePage = () => {
  const { filteredProjects, loading, filters, updateFilters } = useProjects();
  const [selectedProject, setSelectedProject] = useState(null);
  const [showFilterPanel, setShowFilterPanel] = useState(false);
  const [mapCenter] = useState([12.9716, 77.5946]);
  const [currentView, setCurrentView] = useState('hero'); // 'hero', 'map', 'features'

  // Handle loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        <span className="ml-2 text-gray-600">Loading projects...</span>
      </div>
    );
  }

  const getMarkerColor = (status) => {
    switch (status) {
      case 'Completed':
        return '#28a745';
      case 'In Progress':
        return '#ffc107';
      case 'Pending':
        return '#dc3545';
      default:
        return '#6c757d';
    }
  };

  // const getRiskColor = (risk) => {
  //   switch (risk) {
  //     case 'High':
  //       return '#dc3545';
  //     case 'Medium':
  //       return '#ffc107';
  //     case 'Low':
  //       return '#28a745';
  //     default:
  //       return '#6c757d';
  //   }
  // };

  const getProjectMarkers = () => {
    return filteredProjects.map(project => ({
      lat: project.geoPoint?.latitude || 0,
      lng: project.geoPoint?.longitude || 0,
      name: project.projectName || 'Unknown Project',
      description: project.description || 'No description available',
      status: project.status,
      color: getMarkerColor(project.status),
      radius: 500
    })).filter(marker => marker.lat !== 0 && marker.lng !== 0);
  };

  const handleLocationSelect = (location) => {
    // Find projects near the selected location
    const nearbyProjects = filteredProjects.filter(project => {
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

  // Hero Section
  if (currentView === 'hero') {
  return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <div className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <MapPin className="h-8 w-8 text-blue-600" />
                <h1 className="text-2xl font-bold text-gray-900">Janata Audit Bengaluru</h1>
              </div>
              <div className="flex space-x-4">
                <button
                  onClick={() => setCurrentView('map')}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  View Map
                </button>
                <Link
                  to="/projects"
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                >
                  Project Tracking
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Hero Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              AI-Powered Civic Accountability Platform
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Track local government infrastructure projects, public funds, and political donations in Bengaluru with real-time AI analysis using free APIs.
            </p>
          </div>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            {/* Project Tracking Card */}
            <Link
              to="/projects"
              className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer group"
            >
              <div className="flex items-center mb-4">
                <div className="p-3 bg-blue-100 rounded-lg group-hover:bg-blue-200 transition-colors">
                  <MapPin className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 ml-4">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">Project</span> Tracking
                </h3>
              </div>
              <p className="text-gray-600 mb-4">
                Monitor infrastructure projects across Bengaluru with real-time updates
              </p>
              <div className="flex items-center text-blue-600 group-hover:text-blue-700">
                <span className="text-sm font-medium">Explore Projects</span>
                <ArrowRight className="h-4 w-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>

            {/* AI Analysis Card */}
            <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer group">
              <div className="flex items-center mb-4">
                <div className="p-3 bg-purple-100 rounded-lg group-hover:bg-purple-200 transition-colors">
                  <Brain className="h-8 w-8 text-purple-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 ml-4">AI Analysis</h3>
                </div>
              <p className="text-gray-600 mb-4">
                Automated anomaly detection and delay prediction using machine learning
              </p>
              <div className="flex items-center text-purple-600 group-hover:text-purple-700">
                <span className="text-sm font-medium">Coming Soon</span>
                <ArrowRight className="h-4 w-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>

            {/* Crowdsourced Feedback Card */}
            <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer group">
              <div className="flex items-center mb-4">
                <div className="p-3 bg-green-100 rounded-lg group-hover:bg-green-200 transition-colors">
                  <Users className="h-8 w-8 text-green-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 ml-4">Crowdsourced Feedback</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Citizen input and photo submissions for better project monitoring
              </p>
              <div className="flex items-center text-green-600 group-hover:text-green-700">
                <span className="text-sm font-medium">Coming Soon</span>
                <ArrowRight className="h-4 w-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          </div>

          {/* Stats Section */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Platform Statistics</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">{filteredProjects.length}</div>
                <div className="text-gray-600">Total Projects</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">
                  {filteredProjects.filter(p => p.status === 'Completed').length}
                </div>
                <div className="text-gray-600">Completed</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-yellow-600">
                  {filteredProjects.filter(p => p.status === 'In Progress').length}
                </div>
                <div className="text-gray-600">In Progress</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">100%</div>
                <div className="text-gray-600">Free APIs</div>
              </div>
            </div>
          </div>
        </div>
              </div>
    );
  }

  // Map View
  if (currentView === 'map') {
    return (
      <div className="relative h-screen">
        {/* OpenStreetMap */}
        <OpenStreetMapView
          center={mapCenter}
          zoom={12}
          onLocationSelect={handleLocationSelect}
          projectMarkers={getProjectMarkers()}
          analysisData={selectedProject?.satelliteAnalysis}
        />

      {/* Filter Toggle Button */}
      <button
        onClick={() => setShowFilterPanel(!showFilterPanel)}
        className="absolute top-4 left-4 z-10 bg-white hover:bg-gray-50 text-gray-700 px-4 py-2 rounded-lg shadow-lg flex items-center space-x-2 transition-colors"
      >
        <Filter className="h-4 w-4" />
        <span>Filters</span>
      </button>

        {/* Back to Hero Button */}
        <button
          onClick={() => setCurrentView('hero')}
          className="absolute top-4 right-4 z-10 bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-blue-700 transition-colors"
        >
          Back to Home
        </button>

      {/* Filter Panel */}
      {showFilterPanel && (
        <div className="absolute top-4 left-4 z-20">
          <FilterPanel
            filters={filters}
            onFiltersChange={updateFilters}
              projects={filteredProjects}
          />
        </div>
      )}

      {/* Project List (Mobile) */}
      <div className="md:hidden absolute bottom-0 left-0 right-0 bg-white max-h-64 overflow-y-auto">
        <div className="p-4 border-t">
          <h3 className="font-bold text-lg mb-3">Projects ({filteredProjects.length})</h3>
          <div className="space-y-2">
            {filteredProjects.slice(0, 5).map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
                onClick={() => setSelectedProject(project)}
              />
            ))}
            {filteredProjects.length > 5 && (
              <p className="text-sm text-gray-500 text-center">
                +{filteredProjects.length - 5} more projects
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Desktop Project List */}
      <div className="hidden md:block absolute top-4 right-4 w-80 max-h-96 overflow-y-auto bg-white rounded-lg shadow-lg">
        <div className="p-4">
          <h3 className="font-bold text-lg mb-3">Projects ({filteredProjects.length})</h3>
          <div className="space-y-2">
            {filteredProjects.slice(0, 10).map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
                onClick={() => setSelectedProject(project)}
              />
            ))}
            {filteredProjects.length > 10 && (
              <p className="text-sm text-gray-500 text-center">
                +{filteredProjects.length - 10} more projects
              </p>
            )}
          </div>
        </div>
        </div>
      </div>
    );
  }

  // Default fallback
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Welcome to Janata Audit Bengaluru</h1>
        <p className="text-gray-600 mb-6">AI-powered civic accountability platform</p>
        <button
          onClick={() => setCurrentView('hero')}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Get Started
        </button>
      </div>
    </div>
  );
};

export default HomePage;
