import React, { useState, useEffect } from 'react';
import OpenStreetMapView from './OpenStreetMapView';

const EnhancedSatelliteAnalysis = ({ projectId, projectData, onAnalysisComplete }) => {
  const [analysisData, setAnalysisData] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [error, setError] = useState(null);
  const [analysisHistory, setAnalysisHistory] = useState([]);

  // Initialize with project data
  useEffect(() => {
    if (projectData?.geoPoint) {
      setSelectedLocation({
        latitude: projectData.geoPoint.latitude,
        longitude: projectData.geoPoint.longitude
      });
    }
  }, [projectData]);

  const handleLocationSelect = (location) => {
    setSelectedLocation(location);
    setAnalysisData(null); // Clear previous analysis
  };

  const startAnalysis = async () => {
    if (!selectedLocation) {
      setError('Please select a location on the map');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      const response = await fetch('/api/analyze-satellite', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          projectId,
          latitude: selectedLocation.latitude,
          longitude: selectedLocation.longitude,
          projectData
        })
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const result = await response.json();
      setAnalysisData(result.analysisReport);
      
      // Add to analysis history
      setAnalysisHistory(prev => [result.analysisReport, ...prev.slice(0, 4)]);
      
      if (onAnalysisComplete) {
        onAnalysisComplete(result.analysisReport);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const generateReport = () => {
    if (!analysisData) return;

    const reportData = {
      projectName: projectData?.projectName || 'Unknown Project',
      analysisDate: new Date().toLocaleString(),
      location: analysisData.location,
      projectStatus: analysisData.project_status,
      timeAnalysis: analysisData.time_analysis,
      recommendations: analysisData.recommendations,
      confidenceScore: analysisData.confidence_score
    };

    // Create downloadable report
    const reportContent = generateReportContent(reportData);
    downloadReport(reportContent, `satellite-analysis-${projectId}-${Date.now()}.html`);
  };

  const generateReportContent = (data) => {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Satellite Analysis Report - ${data.projectName}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        .header { background: #f4f4f4; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .section { margin-bottom: 30px; padding: 15px; border-left: 4px solid #007bff; }
        .status-badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; }
        .status-completed { background: #d4edda; color: #155724; }
        .status-progress { background: #cce5ff; color: #004085; }
        .status-pending { background: #fff3cd; color: #856404; }
        .recommendation { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 4px; }
        .confidence-bar { background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden; }
        .confidence-fill { height: 100%; background: linear-gradient(90deg, #dc3545 0%, #ffc107 50%, #28a745 100%); }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Satellite Analysis Report</h1>
        <h2>${data.projectName}</h2>
        <p><strong>Analysis Date:</strong> ${data.analysisDate}</p>
        <p><strong>Location:</strong> ${data.location.address}</p>
    </div>

    <div class="section">
        <h3>Project Status Analysis</h3>
        <table>
            <tr>
                <th>Status</th>
                <td>
                    <span class="status-badge status-${data.projectStatus.detected_status.toLowerCase().replace(' ', '-')}">
                        ${data.projectStatus.detected_status}
                    </span>
                </td>
            </tr>
            <tr>
                <th>Reported Status</th>
                <td>${data.projectStatus.reported_status}</td>
            </tr>
            <tr>
                <th>Confidence</th>
                <td>${(data.projectStatus.confidence * 100).toFixed(1)}%</td>
            </tr>
            <tr>
                <th>Status Mismatch</th>
                <td>${data.projectStatus.mismatch ? 'Yes' : 'No'}</td>
            </tr>
        </table>
    </div>

    <div class="section">
        <h3>Time Analysis</h3>
        <table>
            <tr>
                <th>Duration (Months)</th>
                <td>${data.timeAnalysis.total_duration_months.toFixed(1)}</td>
            </tr>
            <tr>
                <th>Completion Percentage</th>
                <td>${data.timeAnalysis.completion_percentage.toFixed(1)}%</td>
            </tr>
            <tr>
                <th>Expected Completion</th>
                <td>${data.timeAnalysis.expected_completion.toFixed(1)}%</td>
            </tr>
            <tr>
                <th>On Track</th>
                <td>${data.timeAnalysis.on_track ? 'Yes' : 'No'}</td>
            </tr>
        </table>
    </div>

    <div class="section">
        <h3>Analysis Confidence</h3>
        <div class="confidence-bar">
            <div class="confidence-fill" style="width: ${data.confidenceScore * 100}%"></div>
        </div>
        <p>Confidence Score: ${(data.confidenceScore * 100).toFixed(1)}%</p>
    </div>

    <div class="section">
        <h3>Recommendations</h3>
        ${data.recommendations.map(rec => `<div class="recommendation">${rec}</div>`).join('')}
    </div>

    <div class="section">
        <h3>Technical Details</h3>
        <p><strong>Location Coordinates:</strong> ${data.location.latitude}, ${data.location.longitude}</p>
        <p><strong>City:</strong> ${data.location.city}</p>
        <p><strong>State:</strong> ${data.location.state}</p>
    </div>
</body>
</html>
    `;
  };

  const downloadReport = (content, filename) => {
    const blob = new Blob([content], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const projectMarkers = projectData?.geoPoint ? [{
    lat: projectData.geoPoint.latitude,
    lng: projectData.geoPoint.longitude,
    name: projectData.projectName || 'Project Location',
    description: projectData.description || 'Project location for analysis',
    status: projectData.status,
    color: 'blue'
  }] : [];

  return (
    <div className="w-full h-full flex flex-col">
      {/* Header */}
      <div className="bg-white p-4 border-b">
        <h2 className="text-xl font-semibold">Enhanced Satellite Analysis</h2>
        <p className="text-gray-600">AI-powered project location analysis using free satellite imagery</p>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Map Section */}
        <div className="flex-1 p-4">
          <div className="h-full border rounded-lg overflow-hidden">
            <OpenStreetMapView
              center={selectedLocation ? [selectedLocation.latitude, selectedLocation.longitude] : [12.9716, 77.5946]}
              zoom={15}
              onLocationSelect={handleLocationSelect}
              onAnalysisStart={startAnalysis}
              analysisData={analysisData}
              projectMarkers={projectMarkers}
            />
          </div>
        </div>

        {/* Analysis Panel */}
        <div className="w-96 bg-gray-50 p-4 overflow-y-auto">
          <div className="space-y-4">
            {/* Analysis Controls */}
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="font-semibold mb-2">Analysis Controls</h3>
              <button
                onClick={startAnalysis}
                disabled={isAnalyzing || !selectedLocation}
                className="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isAnalyzing ? 'Analyzing...' : 'Start AI Analysis'}
              </button>
              {selectedLocation && (
                <p className="text-sm text-gray-600 mt-2">
                  Selected: {selectedLocation.latitude.toFixed(6)}, {selectedLocation.longitude.toFixed(6)}
                </p>
              )}
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            {/* Current Analysis Results */}
            {analysisData && (
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold mb-2">Analysis Results</h3>
                
                <div className="space-y-3">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Detected Status</label>
                    <div className={`inline-block px-2 py-1 rounded text-xs ${
                      analysisData.project_status.detected_status === 'Completed' ? 'bg-green-100 text-green-800' :
                      analysisData.project_status.detected_status === 'In Progress' ? 'bg-blue-100 text-blue-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {analysisData.project_status.detected_status}
                    </div>
                  </div>

                  <div>
                    <label className="text-sm font-medium text-gray-700">Confidence</label>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{ width: `${analysisData.confidence_score * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-600">
                      {(analysisData.confidence_score * 100).toFixed(1)}%
                    </span>
                  </div>

                  <div>
                    <label className="text-sm font-medium text-gray-700">Duration</label>
                    <p className="text-sm">{analysisData.time_analysis.total_duration_months.toFixed(1)} months</p>
                  </div>

                  <div>
                    <label className="text-sm font-medium text-gray-700">Completion</label>
                    <p className="text-sm">{analysisData.time_analysis.completion_percentage.toFixed(1)}%</p>
                  </div>

                  {analysisData.project_status.mismatch && (
                    <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-3 py-2 rounded text-sm">
                      ⚠️ Status mismatch detected
                    </div>
                  )}

                  <button
                    onClick={generateReport}
                    className="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 text-sm"
                  >
                    Download Report
                  </button>
                </div>
              </div>
            )}

            {/* Analysis History */}
            {analysisHistory.length > 0 && (
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold mb-2">Analysis History</h3>
                <div className="space-y-2">
                  {analysisHistory.slice(0, 3).map((analysis, index) => (
                    <div key={index} className="text-sm border-l-2 border-gray-200 pl-2">
                      <div className="font-medium">
                        {new Date(analysis.analysis_timestamp).toLocaleString()}
                      </div>
                      <div className="text-gray-600">
                        Status: {analysis.project_status.detected_status} | 
                        Confidence: {(analysis.confidence_score * 100).toFixed(0)}%
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Free APIs Info */}
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold mb-2 text-blue-800">Free APIs Used</h3>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• OpenStreetMap (Mapping)</li>
                <li>• Esri World Imagery (Satellite)</li>
                <li>• Nominatim (Geocoding)</li>
                <li>• Computer Vision Analysis</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedSatelliteAnalysis;
