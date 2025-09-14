import React, { useState, useEffect } from 'react';
import { triggerSatelliteAnalysis, getSatelliteAnalysis } from '../services/api';
import { 
  Satellite, 
  MapPin, 
  Calendar, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle,
  Clock,
  BarChart3
} from 'lucide-react';
import OpenStreetMapView from './OpenStreetMapView';

const SatelliteAnalysis = ({ projectId, projectData }) => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (projectId) {
      fetchAnalysis();
    }
  }, [projectId]);

  const fetchAnalysis = async () => {
    try {
      setLoading(true);
      const result = await getSatelliteAnalysis(projectId);
      
      if (result.success) {
        setAnalysis(result.results);
      } else {
        setAnalysis(null);
      }
    } catch (err) {
      console.error('Error fetching satellite analysis:', err);
      setError('Failed to fetch satellite analysis');
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await triggerSatelliteAnalysis(projectId, projectData);
      
      if (result.success) {
        // Wait a moment and then fetch the updated analysis
        setTimeout(() => {
          fetchAnalysis();
        }, 2000);
      }
    } catch (err) {
      console.error('Error triggering satellite analysis:', err);
      setError('Failed to trigger satellite analysis');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'high':
        return 'text-red-600 bg-red-50';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50';
      case 'low':
        return 'text-green-600 bg-green-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'high':
        return <AlertTriangle className="h-4 w-4" />;
      case 'medium':
        return <Clock className="h-4 w-4" />;
      case 'low':
        return <CheckCircle className="h-4 w-4" />;
      default:
        return <BarChart3 className="h-4 w-4" />;
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading && !analysis) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex items-center justify-center py-8">
          <div className="loading-spinner"></div>
          <span className="ml-2 text-gray-600">Loading satellite analysis...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="text-center py-8">
          <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Analysis Error</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={handleTriggerAnalysis}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Retry Analysis
          </button>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="text-center py-8">
          <Satellite className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Satellite Analysis</h3>
          <p className="text-gray-600 mb-4">
            Satellite analysis has not been performed for this project yet.
          </p>
          <button
            onClick={handleTriggerAnalysis}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Run Satellite Analysis'}
          </button>
        </div>
      </div>
    );
  }

  const analysisResult = analysis.analysisResult || {};
  const isMismatch = analysisResult.isMismatch || false;
  const severity = analysisResult.severity || 'low';

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <Satellite className="h-6 w-6 text-blue-600 mr-2" />
          <h3 className="text-xl font-semibold text-gray-900">Satellite Analysis</h3>
        </div>
        <div className="flex items-center space-x-2">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(severity)}`}>
            {getStatusIcon(severity)}
            <span className="ml-1 capitalize">{severity} Risk</span>
          </span>
          <button
            onClick={handleTriggerAnalysis}
            disabled={loading}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            {loading ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>
      </div>

      {/* Analysis Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center">
            <TrendingUp className="h-5 w-5 text-blue-600 mr-2" />
            <div>
              <p className="text-sm text-gray-600">NDBI Change</p>
              <p className="text-lg font-semibold text-gray-900">
                {analysis.ndbiChangePercent?.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center">
            <MapPin className="h-5 w-5 text-green-600 mr-2" />
            <div>
              <p className="text-sm text-gray-600">Analysis Area</p>
              <p className="text-lg font-semibold text-gray-900">
                {analysis.roiBuffer}m radius
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center">
            <Calendar className="h-5 w-5 text-purple-600 mr-2" />
            <div>
              <p className="text-sm text-gray-600">Last Analysis</p>
              <p className="text-lg font-semibold text-gray-900">
                {formatDate(analysis.analysisDate)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* OpenStreetMap Integration */}
      <div className="mb-6">
        <OpenStreetMapView center={[12.9716, 77.5946]} zoom={13} />
      </div>

      {/* Mismatch Alert */}
      {isMismatch && (
        <div className={`mb-6 p-4 rounded-lg border-l-4 ${
          severity === 'high' ? 'bg-red-50 border-red-400' :
          severity === 'medium' ? 'bg-yellow-50 border-yellow-400' :
          'bg-orange-50 border-orange-400'
        }`}>
          <div className="flex items-start">
            <AlertTriangle className={`h-5 w-5 mt-0.5 mr-3 ${
              severity === 'high' ? 'text-red-500' :
              severity === 'medium' ? 'text-yellow-500' :
              'text-orange-500'
            }`} />
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Verification Mismatch Detected</h4>
              <p className="text-sm text-gray-700">
                {analysisResult.mismatchReason || 'Physical changes detected do not match project status claims.'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Detailed Analysis */}
      <div className="space-y-4">
        <h4 className="font-semibold text-gray-900">Analysis Details</h4>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <h5 className="font-medium text-gray-900 mb-2">Before Period</h5>
            <p className="text-sm text-gray-600">
              Mean NDBI: {analysis.beforeMeanNDBI?.toFixed(3)}
            </p>
            <p className="text-sm text-gray-600">
              Period: {analysis.timePeriods?.before}
            </p>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <h5 className="font-medium text-gray-900 mb-2">After Period</h5>
            <p className="text-sm text-gray-600">
              Mean NDBI: {analysis.afterMeanNDBI?.toFixed(3)}
            </p>
            <p className="text-sm text-gray-600">
              Period: {analysis.timePeriods?.after}
            </p>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4">
          <h5 className="font-medium text-gray-900 mb-2">Project Context</h5>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Status:</span>
              <span className="ml-2 font-medium">{analysis.projectStatus}</span>
            </div>
            <div>
              <span className="text-gray-600">Duration:</span>
              <span className="ml-2 font-medium">
                {analysisResult.projectDurationMonths?.toFixed(1)} months
              </span>
            </div>
            <div>
              <span className="text-gray-600">Confidence:</span>
              <span className="ml-2 font-medium capitalize">
                {analysisResult.confidence || 'Unknown'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Technical Details */}
      <details className="mt-6">
        <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
          Technical Details
        </summary>
        <div className="mt-2 p-4 bg-gray-50 rounded-lg text-sm text-gray-600">
          <p className="mb-2">
            <strong>NDBI (Normalized Difference Built-up Index):</strong> Measures the presence of built-up structures 
            using satellite imagery. Higher values indicate more concrete, asphalt, and buildings.
          </p>
          <p className="mb-2">
            <strong>Data Source:</strong> Sentinel-2 satellite imagery from Google Earth Engine
          </p>
          <p className="mb-2">
            <strong>Analysis Method:</strong> Comparison of NDBI values before and after project start date
          </p>
          <p>
            <strong>Cloud Filtering:</strong> Only images with less than 20% cloud cover are used for analysis
          </p>
        </div>
      </details>
    </div>
  );
};

export default SatelliteAnalysis;
