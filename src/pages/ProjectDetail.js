import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useProjects } from '../contexts/ProjectContext';
import { useAuth } from '../contexts/AuthContext';
import { 
  ArrowLeft, 
  MapPin, 
  Calendar, 
  DollarSign, 
  Building, 
  AlertTriangle,
  MessageCircle,
  Camera,
  Star,
  Send
} from 'lucide-react';
import SatelliteAnalysis from '../components/SatelliteAnalysis';

const ProjectDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { getProjectById, getProjectFeedback, submitProjectFeedback, loading: projectsLoading } = useProjects();
  const { currentUser, loading: authLoading } = useAuth();
  const [project, setProject] = useState(null);
  const [feedback, setFeedback] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [newFeedback, setNewFeedback] = useState({
    comment: '',
    rating: '5',
    photoURL: ''
  });

  // Handle loading state
  if (authLoading || projectsLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        <span className="ml-2 text-gray-600">Loading...</span>
      </div>
    );
  }

  useEffect(() => {
    const fetchProjectData = async () => {
      try {
        const projectData = await getProjectById(id);
        if (projectData) {
          setProject(projectData);
        } else {
          navigate('/');
        }
      } catch (error) {
        console.error('Error fetching project:', error);
        navigate('/');
      }
    };

    const fetchFeedback = async () => {
      try {
        const feedbackData = await getProjectFeedback(id);
        setFeedback(feedbackData);
      } catch (error) {
        console.error('Error fetching feedback:', error);
      }
    };

    fetchProjectData();
    fetchFeedback();
    setLoading(false);
  }, [id, getProjectById, getProjectFeedback, navigate]);

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    if (!currentUser) {
      alert('Please sign in to submit feedback');
      return;
    }

    try {
      await submitProjectFeedback(id, newFeedback);
      setNewFeedback({ comment: '', rating: '5', photoURL: '' });
      setShowFeedbackForm(false);
      // Refresh feedback list
      const feedbackData = await getProjectFeedback(id);
      setFeedback(feedbackData);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    }
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return 'N/A';
    const date = timestamp.toDate ? timestamp.toDate() : new Date(timestamp);
    return date.toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatBudget = (budget) => {
    if (!budget) return 'N/A';
    const num = parseFloat(budget.replace(/[^\d.]/g, ''));
    if (num >= 10000000) {
      return `₹${(num / 10000000).toFixed(1)} Crore`;
    } else if (num >= 100000) {
      return `₹${(num / 100000).toFixed(1)} Lakh`;
    } else {
      return `₹${num.toLocaleString('en-IN')}`;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Completed':
        return 'bg-green-100 text-green-800';
      case 'In Progress':
        return 'bg-yellow-100 text-yellow-800';
      case 'Pending':
        return 'bg-red-100 text-red-800';
      case 'Cancelled':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'High':
        return 'text-red-600 bg-red-50';
      case 'Medium':
        return 'text-yellow-600 bg-yellow-50';
      case 'Low':
        return 'text-green-600 bg-green-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="loading-spinner"></div>
        <span className="ml-2 text-gray-600">Loading project details...</span>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Project Not Found</h2>
          <p className="text-gray-600 mb-4">The project you're looking for doesn't exist.</p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Go Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/')}
              className="flex items-center text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="h-5 w-5 mr-2" />
              Back to Map
            </button>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(project.status)}`}>
              {project.status}
            </span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Project Header */}
            <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                {project.projectName}
              </h1>
              <p className="text-gray-600 text-lg mb-6">
                {project.description}
              </p>

              {/* Project Details Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex items-center">
                  <MapPin className="h-5 w-5 text-gray-400 mr-3" />
                  <div>
                    <p className="text-sm text-gray-500">Ward</p>
                    <p className="font-medium">{project.wardNumber}</p>
                  </div>
                </div>

                <div className="flex items-center">
                  <Building className="h-5 w-5 text-gray-400 mr-3" />
                  <div>
                    <p className="text-sm text-gray-500">Department</p>
                    <p className="font-medium">{project.department}</p>
                  </div>
                </div>

                <div className="flex items-center">
                  <Calendar className="h-5 w-5 text-gray-400 mr-3" />
                  <div>
                    <p className="text-sm text-gray-500">Start Date</p>
                    <p className="font-medium">{formatDate(project.startDate)}</p>
                  </div>
                </div>

                <div className="flex items-center">
                  <Calendar className="h-5 w-5 text-gray-400 mr-3" />
                  <div>
                    <p className="text-sm text-gray-500">Expected End Date</p>
                    <p className="font-medium">{formatDate(project.endDate)}</p>
                  </div>
                </div>

                <div className="flex items-center">
                  <DollarSign className="h-5 w-5 text-gray-400 mr-3" />
                  <div>
                    <p className="text-sm text-gray-500">Budget</p>
                    <p className="font-medium">{formatBudget(project.budget)}</p>
                  </div>
                </div>

                {project.contractorName && (
                  <div className="flex items-center">
                    <Building className="h-5 w-5 text-gray-400 mr-3" />
                    <div>
                      <p className="text-sm text-gray-500">Contractor</p>
                      <p className="font-medium">{project.contractorName}</p>
                    </div>
                  </div>
                )}
              </div>

            {/* AI Risk Assessment */}
            {project.predictedDelayRisk && (
              <div className={`mt-6 p-4 rounded-lg ${getRiskColor(project.predictedDelayRisk)}`}>
                <div className="flex items-center">
                  <AlertTriangle className="h-5 w-5 mr-2" />
                  <h3 className="font-semibold">AI Delay Risk Assessment</h3>
                </div>
                <p className="mt-2 text-sm">
                  Based on historical data and project characteristics, this project has a{' '}
                  <span className="font-semibold">{project.predictedDelayRisk}</span> risk of delay.
                </p>
              </div>
            )}

            {/* Satellite Analysis */}
            <div className="mt-6">
              <SatelliteAnalysis projectId={id} projectData={project} />
            </div>
            </div>

            {/* Feedback Section */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900 flex items-center">
                  <MessageCircle className="h-5 w-5 mr-2" />
                  Community Feedback ({feedback.length})
                </h2>
                {currentUser && (
                  <button
                    onClick={() => setShowFeedbackForm(!showFeedbackForm)}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center"
                  >
                    <MessageCircle className="h-4 w-4 mr-2" />
                    Add Feedback
                  </button>
                )}
              </div>

              {/* Feedback Form */}
              {showFeedbackForm && (
                <form onSubmit={handleFeedbackSubmit} className="mb-6 p-4 bg-gray-50 rounded-lg">
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Rating
                    </label>
                    <select
                      value={newFeedback.rating}
                      onChange={(e) => setNewFeedback({ ...newFeedback, rating: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="1">1 - Poor</option>
                      <option value="2">2 - Fair</option>
                      <option value="3">3 - Good</option>
                      <option value="4">4 - Very Good</option>
                      <option value="5">5 - Excellent</option>
                    </select>
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Comment
                    </label>
                    <textarea
                      value={newFeedback.comment}
                      onChange={(e) => setNewFeedback({ ...newFeedback, comment: e.target.value })}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Share your thoughts about this project..."
                      required
                    />
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Photo URL (Optional)
                    </label>
                    <input
                      type="url"
                      value={newFeedback.photoURL}
                      onChange={(e) => setNewFeedback({ ...newFeedback, photoURL: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="https://example.com/photo.jpg"
                    />
                  </div>
                  <div className="flex justify-end space-x-3">
                    <button
                      type="button"
                      onClick={() => setShowFeedbackForm(false)}
                      className="px-4 py-2 text-gray-600 hover:text-gray-800"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center"
                    >
                      <Send className="h-4 w-4 mr-2" />
                      Submit
                    </button>
                  </div>
                </form>
              )}

              {/* Feedback List */}
              <div className="space-y-4">
                {feedback.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">
                    No feedback yet. Be the first to share your thoughts!
                  </p>
                ) : (
                  feedback.map((item) => (
                    <div key={item.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center">
                          <div className="flex items-center">
                            {[...Array(5)].map((_, i) => (
                              <Star
                                key={i}
                                className={`h-4 w-4 ${
                                  i < parseInt(item.rating)
                                    ? 'text-yellow-400 fill-current'
                                    : 'text-gray-300'
                                }`}
                              />
                            ))}
                          </div>
                          <span className="ml-2 text-sm text-gray-500">
                            {item.rating}/5
                          </span>
                        </div>
                        <span className="text-sm text-gray-500">
                          {formatDate(item.timestamp)}
                        </span>
                      </div>
                      <p className="text-gray-700 mb-3">{item.comment}</p>
                      {item.photoURL && (
                        <img
                          src={item.photoURL}
                          alt="Feedback photo"
                          className="w-full max-w-md rounded-lg"
                          onError={(e) => {
                            e.target.style.display = 'none';
                          }}
                        />
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            {/* Map Placeholder */}
            <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Location</h3>
              <div className="bg-gray-200 h-48 rounded-lg flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <MapPin className="h-8 w-8 mx-auto mb-2" />
                  <p>Interactive Map</p>
                  <p className="text-sm">Ward: {project.wardNumber}</p>
                </div>
              </div>
            </div>

            {/* Project Stats */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Statistics</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Status</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                    {project.status}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Feedback Count</span>
                  <span className="font-medium">{feedback.length}</span>
                </div>
                {project.actualCompletionDate && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Actual Completion</span>
                    <span className="font-medium">{formatDate(project.actualCompletionDate)}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectDetail;
