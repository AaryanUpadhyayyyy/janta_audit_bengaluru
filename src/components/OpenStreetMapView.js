import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap, LayersControl } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Custom satellite tile layer
const SatelliteLayer = () => (
  <TileLayer
    url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attribution='&copy; <a href="https://www.esri.com/">Esri</a> — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
  />
);

// Custom OSM layer
const OSMLayer = () => (
    <TileLayer
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    />
);

// Custom CartoDB layer
const CartoDBLayer = () => (
  <TileLayer
    url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
  />
);

// Map controls component
const MapControls = ({ onLocationSelect, onAnalysisStart, analysisData }) => {
  const map = useMap();
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    const handleClick = (e) => {
      const { lat, lng } = e.latlng;
      onLocationSelect({ latitude: lat, longitude: lng });
    };

    map.on('click', handleClick);
    return () => map.off('click', handleClick);
  }, [map, onLocationSelect]);

  const startAnalysis = async () => {
    setIsAnalyzing(true);
    try {
      await onAnalysisStart();
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="absolute top-4 right-4 z-[1000] bg-white p-4 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold mb-2">Map Controls</h3>
      <button
        onClick={startAnalysis}
        disabled={isAnalyzing}
        className="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {isAnalyzing ? 'Analyzing...' : 'Start AI Analysis'}
      </button>
      {analysisData && (
        <div className="mt-4 p-3 bg-gray-100 rounded">
          <h4 className="font-semibold">Analysis Results:</h4>
          <p className="text-sm">Status: {analysisData.status}</p>
          <p className="text-sm">Confidence: {analysisData.confidence}%</p>
          <p className="text-sm">Time Period: {analysisData.timePeriod}</p>
        </div>
      )}
    </div>
  );
};

const OpenStreetMapView = ({ 
  center = [12.9716, 77.5946], 
  zoom = 13, 
  onLocationSelect = () => {},
  onAnalysisStart = () => {},
  analysisData = null,
  projectMarkers = [],
  showSatellite = false
}) => {
  const [mapCenter, setMapCenter] = useState(center);
  const [mapZoom, setMapZoom] = useState(zoom);

  // Update map center when prop changes
  useEffect(() => {
    setMapCenter(center);
    setMapZoom(zoom);
  }, [center, zoom]);

  return (
    <div className="w-full h-full relative">
      <MapContainer 
        center={mapCenter} 
        zoom={mapZoom} 
        style={{ height: '100%', width: '100%' }}
        className="rounded-lg"
      >
        <LayersControl position="topright">
          <LayersControl.BaseLayer checked name="OpenStreetMap">
            <OSMLayer />
          </LayersControl.BaseLayer>
          <LayersControl.BaseLayer name="Satellite">
            <SatelliteLayer />
          </LayersControl.BaseLayer>
          <LayersControl.BaseLayer name="CartoDB Light">
            <CartoDBLayer />
          </LayersControl.BaseLayer>
        </LayersControl>

        {/* Project markers */}
        {projectMarkers.map((marker, index) => (
          <Marker key={index} position={[marker.lat, marker.lng]}>
            <Popup>
              <div>
                <h3 className="font-semibold">{marker.name}</h3>
                <p className="text-sm">{marker.description}</p>
                {marker.status && (
                  <span className={`inline-block px-2 py-1 rounded text-xs ${
                    marker.status === 'Completed' ? 'bg-green-100 text-green-800' :
                    marker.status === 'In Progress' ? 'bg-blue-100 text-blue-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {marker.status}
                  </span>
                )}
              </div>
            </Popup>
            {marker.radius && (
              <Circle
                center={[marker.lat, marker.lng]}
                radius={marker.radius}
                pathOptions={{
                  color: marker.color || 'blue',
                  fillColor: marker.color || 'blue',
                  fillOpacity: 0.2
                }}
              />
            )}
    </Marker>
        ))}

        {/* Analysis area circle */}
        {analysisData && analysisData.analysisArea && (
          <Circle
            center={[analysisData.analysisArea.lat, analysisData.analysisArea.lng]}
            radius={analysisData.analysisArea.radius || 500}
            pathOptions={{
              color: 'red',
              fillColor: 'red',
              fillOpacity: 0.1
            }}
          />
        )}

        <MapControls 
          onLocationSelect={onLocationSelect}
          onAnalysisStart={onAnalysisStart}
          analysisData={analysisData}
        />
  </MapContainer>
    </div>
);
};

export default OpenStreetMapView;
