import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MapPin, Calendar, DollarSign, User, Building, AlertTriangle, CheckCircle, Clock, ArrowLeft, Satellite, BarChart3, Download, Share2 } from 'lucide-react';
import OpenStreetMapView from './OpenStreetMapView';
import EnhancedSatelliteAnalysis from './EnhancedSatelliteAnalysis';

const ProjectDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [satelliteAnalysis, setSatelliteAnalysis] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);

  const fetchProjectDetails = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/projects/${id}`);
      if (response.ok) {
        const projectData = await response.json();
        setProject(projectData);
      } else {
        console.error('Failed to fetch project details');
      }
    } catch (error) {
      console.error('Error fetching project details:', error);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchProjectDetails();
  }, [fetchProjectDetails]);

  // Handle loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        <span className="ml-2 text-gray-600">Loading project details...</span>
      </div>
    );
  }

  const handleSatelliteAnalysis = async () => {
    if (!project) return;
    
    setAnalysisLoading(true);
    try {
      const response = await fetch('/api/satellite/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          projectId: project.id,
          location: {
            latitude: project.geoPoint?.latitude || 12.9716,
            longitude: project.geoPoint?.longitude || 77.5946
          },
          projectName: project.projectName
        })
      });

      if (response.ok) {
        const analysis = await response.json();
        setSatelliteAnalysis(analysis);
        setActiveTab('satellite');
      }
    } catch (error) {
      console.error('Error running satellite analysis:', error);
    } finally {
      setAnalysisLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'In Progress':
        return <Clock className="h-5 w-5 text-blue-500" />;
      case 'Pending':
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Completed':
        return 'bg-green-100 text-green-800';
      case 'In Progress':
        return 'bg-blue-100 text-blue-800';
      case 'Pending':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatCurrency = (amount) => {
    if (!amount) return 'Not specified';
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not specified';
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading project details...</p>
        </div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Project Not Found</h1>
          <p className="text-gray-600 mb-6">The project you're looking for doesn't exist.</p>
          <button
            onClick={() => navigate('/projects')}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Back to Projects
          </button>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'map', label: 'Map View', icon: MapPin },
    { id: 'satellite', label: 'Satellite Analysis', icon: Satellite },
    { id: 'documents', label: 'Documents', icon: Download }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/projects')}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="h-5 w-5 text-gray-600" />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{project.projectName}</h1>
                <p className="text-gray-600">{project.department} • {project.location}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <Share2 className="h-5 w-5 text-gray-600" />
              </button>
              <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <Download className="h-5 w-5 text-gray-600" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-6">
              {/* Project Status Card */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-900">Project Status</h2>
                  <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(project.status)}`}>
                    {getStatusIcon(project.status)}
                    <span>{project.status}</span>
                  </div>
                </div>
                <p className="text-gray-600">{project.description}</p>
              </div>

              {/* Project Details */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Project Details</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <DollarSign className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-500">Budget</p>
                        <p className="text-lg font-semibold text-gray-900">{formatCurrency(project.budget)}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <Calendar className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-500">Start Date</p>
                        <p className="text-lg font-semibold text-gray-900">{formatDate(project.startDate)}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <Calendar className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-500">End Date</p>
                        <p className="text-lg font-semibold text-gray-900">{formatDate(project.endDate)}</p>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <Building className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-500">Department</p>
                        <p className="text-lg font-semibold text-gray-900">{project.department}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <MapPin className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-500">Location</p>
                        <p className="text-lg font-semibold text-gray-900">{project.location}</p>
                      </div>
                    </div>
                    {project.contractor && (
                      <div className="flex items-center space-x-3">
                        <User className="h-5 w-5 text-gray-400" />
                        <div>
                          <p className="text-sm font-medium text-gray-500">Contractor</p>
                          <p className="text-lg font-semibold text-gray-900">{project.contractor}</p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* AI Analysis Results */}
              {project.aiAnalysis && (
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Analysis Results</h2>
                  <div className="space-y-4">
                    {project.aiAnalysis.anomalies?.map((anomaly, index) => (
                      <div key={index} className="flex items-start space-x-3 p-3 bg-yellow-50 rounded-lg">
                        <AlertTriangle className="h-5 w-5 text-yellow-500 mt-0.5" />
                        <div>
                          <p className="font-medium text-yellow-800">{anomaly.type}</p>
                          <p className="text-sm text-yellow-700">{anomaly.description}</p>
                          <p className="text-xs text-yellow-600 mt-1">Confidence: {anomaly.confidence}%</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Quick Actions */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  <button
                    onClick={handleSatelliteAnalysis}
                    disabled={analysisLoading}
                    className="w-full flex items-center justify-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                  >
                    <Satellite className="h-4 w-4" />
                    <span>{analysisLoading ? 'Analyzing...' : 'Run Satellite Analysis'}</span>
                  </button>
                  <button className="w-full flex items-center justify-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                    <Download className="h-4 w-4" />
                    <span>Download Report</span>
                  </button>
                </div>
              </div>

              {/* Project Timeline */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Timeline</h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Project Started</p>
                      <p className="text-xs text-gray-500">{formatDate(project.startDate)}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Current Status</p>
                      <p className="text-xs text-gray-500">{project.status}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Expected Completion</p>
                      <p className="text-xs text-gray-500">{formatDate(project.endDate)}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Source Information */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Source Information</h3>
                <div className="space-y-2">
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Source:</span> {project.source}
                  </p>
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Last Updated:</span> {formatDate(project.scrapedAt)}
                  </p>
                  {project.sourceUrl && (
                    <a
                      href={project.sourceUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 text-sm"
                    >
                      View Original Source
                    </a>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'map' && (
          <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
            <div className="h-96">
              <OpenStreetMapView
                center={[project.geoPoint?.latitude || 12.9716, project.geoPoint?.longitude || 77.5946]}
                zoom={15}
                projectMarkers={[{
                  lat: project.geoPoint?.latitude || 12.9716,
                  lng: project.geoPoint?.longitude || 77.5946,
                  name: project.projectName,
                  description: project.description,
                  status: project.status,
                  color: project.status === 'Completed' ? '#28a745' : project.status === 'In Progress' ? '#ffc107' : '#dc3545',
                  radius: 500
                }]}
                analysisData={satelliteAnalysis}
              />
            </div>
          </div>
        )}

        {activeTab === 'satellite' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Satellite Imagery Analysis</h2>
              <p className="text-gray-600 mb-6">
                AI-powered analysis of satellite imagery to assess project progress and detect changes over time.
              </p>
              
              {satelliteAnalysis ? (
                <EnhancedSatelliteAnalysis
                  projectId={project.id}
                  projectName={project.projectName}
                  location={{
                    latitude: project.geoPoint?.latitude || 12.9716,
                    longitude: project.geoPoint?.longitude || 77.5946
                  }}
                />
              ) : (
                <div className="text-center py-12">
                  <Satellite className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No Analysis Available</h3>
                  <p className="text-gray-600 mb-6">Run satellite analysis to get AI-powered insights about this project.</p>
                  <button
                    onClick={handleSatelliteAnalysis}
                    disabled={analysisLoading}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                  >
                    {analysisLoading ? 'Analyzing...' : 'Start Analysis'}
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'documents' && (
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Project Documents</h2>
            <div className="text-center py-12">
              <Download className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Documents Available</h3>
              <p className="text-gray-600">Documents will be available once they are uploaded or linked from the source portal.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectDetailPage;
