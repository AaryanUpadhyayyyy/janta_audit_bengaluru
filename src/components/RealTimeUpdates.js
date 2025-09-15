import React, { useState, useEffect, useCallback } from 'react';
import { 
  Bell, 
  CheckCircle, 
  AlertTriangle, 
  Info, 
  X, 
  RefreshCw,
  Activity,
  MapPin,
  DollarSign,
  Calendar
} from 'lucide-react';

const RealTimeUpdates = ({ projects = [], onProjectUpdate }) => {
  const [notifications, setNotifications] = useState([]);
  const [isConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [updateInterval, setUpdateInterval] = useState(30000); // 30 seconds
  const [isAutoRefresh, setIsAutoRefresh] = useState(true);

  // Simulate real-time updates
  useEffect(() => {
    if (!isAutoRefresh) return;

    const interval = setInterval(() => {
      checkForUpdates();
    }, updateInterval);

    return () => clearInterval(interval);
  }, [isAutoRefresh, updateInterval, projects, checkForUpdates]);

  const checkForUpdates = useCallback(async () => {
    try {
      // Simulate checking for updates
      const updates = await simulateProjectUpdates(projects);
      
      if (updates.length > 0) {
        setNotifications(prev => [...updates, ...prev].slice(0, 50)); // Keep last 50 notifications
        setLastUpdate(new Date());
        
        // Notify parent component of updates
        if (onProjectUpdate) {
          onProjectUpdate(updates);
        }
      }
    } catch (error) {
      console.error('Error checking for updates:', error);
    }
  }, [projects, onProjectUpdate, simulateProjectUpdates]);

  const simulateProjectUpdates = useCallback(async (projects) => {
    // Simulate random updates
    const updates = [];
    const updateTypes = [
      'status_change',
      'budget_update',
      'timeline_update',
      'location_update',
      'analysis_complete',
      'delay_alert'
    ];

    // Randomly generate 0-3 updates
    const numUpdates = Math.floor(Math.random() * 4);
    
    for (let i = 0; i < numUpdates; i++) {
      const project = projects[Math.floor(Math.random() * projects.length)];
      if (!project) continue;

      const updateType = updateTypes[Math.floor(Math.random() * updateTypes.length)];
      const update = generateUpdate(project, updateType);
      
      if (update) {
        updates.push(update);
      }
    }

    return updates;
  }, []);

  const generateUpdate = (project, updateType) => {
    const timestamp = new Date();
    const projectName = project.projectName || 'Unknown Project';

    switch (updateType) {
      case 'status_change':
        const newStatus = ['Completed', 'In Progress', 'Pending', 'Delayed'][Math.floor(Math.random() * 4)];
        if (newStatus !== project.status) {
          return {
            id: `update_${Date.now()}_${Math.random()}`,
            type: 'status_change',
            title: 'Project Status Updated',
            message: `${projectName} status changed to ${newStatus}`,
            projectId: project.id,
            projectName,
            timestamp,
            severity: newStatus === 'Delayed' ? 'warning' : 'info',
            icon: newStatus === 'Completed' ? CheckCircle : newStatus === 'Delayed' ? AlertTriangle : Activity
          };
        }
        break;

      case 'budget_update':
        const budgetChange = (Math.random() - 0.5) * 0.2; // ±10% change
        const newBudget = project.budget ? parseFloat(project.budget) * (1 + budgetChange) : 0;
        return {
          id: `update_${Date.now()}_${Math.random()}`,
          type: 'budget_update',
          title: 'Budget Updated',
          message: `${projectName} budget updated to ₹${newBudget.toLocaleString()}`,
          projectId: project.id,
          projectName,
          timestamp,
          severity: budgetChange > 0.1 ? 'warning' : 'info',
          icon: DollarSign
        };

      case 'timeline_update':
        const daysChange = Math.floor((Math.random() - 0.5) * 30); // ±15 days
        return {
          id: `update_${Date.now()}_${Math.random()}`,
          type: 'timeline_update',
          title: 'Timeline Updated',
          message: `${projectName} timeline ${daysChange > 0 ? 'extended' : 'shortened'} by ${Math.abs(daysChange)} days`,
          projectId: project.id,
          projectName,
          timestamp,
          severity: daysChange > 7 ? 'warning' : 'info',
          icon: Calendar
        };

      case 'location_update':
        return {
          id: `update_${Date.now()}_${Math.random()}`,
          type: 'location_update',
          title: 'Location Updated',
          message: `${projectName} location coordinates updated`,
          projectId: project.id,
          projectName,
          timestamp,
          severity: 'info',
          icon: MapPin
        };

      case 'analysis_complete':
        return {
          id: `update_${Date.now()}_${Math.random()}`,
          type: 'analysis_complete',
          title: 'AI Analysis Complete',
          message: `Satellite analysis completed for ${projectName}`,
          projectId: project.id,
          projectName,
          timestamp,
          severity: 'success',
          icon: CheckCircle
        };

      case 'delay_alert':
        return {
          id: `update_${Date.now()}_${Math.random()}`,
          type: 'delay_alert',
          title: 'Project Delay Alert',
          message: `${projectName} is behind schedule by ${Math.floor(Math.random() * 30) + 1} days`,
          projectId: project.id,
          projectName,
          timestamp,
          severity: 'warning',
          icon: AlertTriangle
        };

      default:
        return null;
    }

    return null;
  };

  const dismissNotification = (notificationId) => {
    setNotifications(prev => prev.filter(n => n.id !== notificationId));
  };

  const clearAllNotifications = () => {
    setNotifications([]);
  };

  const refreshNow = () => {
    checkForUpdates();
  };

  const getSeverityColor = (severity) => {
    const colors = {
      info: 'bg-blue-50 border-blue-200 text-blue-800',
      success: 'bg-green-50 border-green-200 text-green-800',
      warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
      error: 'bg-red-50 border-red-200 text-red-800'
    };
    return colors[severity] || colors.info;
  };

  const getSeverityIcon = (severity) => {
    const icons = {
      info: Info,
      success: CheckCircle,
      warning: AlertTriangle,
      error: AlertTriangle
    };
    return icons[severity] || Info;
  };

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <Bell className="h-6 w-6 text-blue-600 mr-2" />
          <h3 className="text-lg font-semibold text-gray-800">Real-Time Updates</h3>
          <div className={`ml-3 w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={refreshNow}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg"
            title="Refresh Now"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
          <button
            onClick={() => setIsAutoRefresh(!isAutoRefresh)}
            className={`px-3 py-1 text-sm rounded ${
              isAutoRefresh 
                ? 'bg-green-100 text-green-800' 
                : 'bg-gray-100 text-gray-600'
            }`}
          >
            {isAutoRefresh ? 'Auto ON' : 'Auto OFF'}
          </button>
        </div>
      </div>

      {/* Status Bar */}
      <div className="mb-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex items-center justify-between text-sm text-gray-600">
          <span>Last update: {lastUpdate ? formatTimeAgo(lastUpdate) : 'Never'}</span>
          <span>Update interval: {updateInterval / 1000}s</span>
          <span>Notifications: {notifications.length}</span>
        </div>
      </div>

      {/* Controls */}
      <div className="mb-4 flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <label className="text-sm text-gray-600">Update Interval:</label>
          <select
            value={updateInterval}
            onChange={(e) => setUpdateInterval(Number(e.target.value))}
            className="px-2 py-1 border border-gray-300 rounded text-sm"
          >
            <option value={10000}>10s</option>
            <option value={30000}>30s</option>
            <option value={60000}>1m</option>
            <option value={300000}>5m</option>
          </select>
        </div>

        {notifications.length > 0 && (
          <button
            onClick={clearAllNotifications}
            className="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded"
          >
            Clear All
          </button>
        )}
      </div>

      {/* Notifications List */}
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {notifications.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <Bell className="h-12 w-12 mx-auto mb-2 text-gray-300" />
            <p>No updates yet</p>
            <p className="text-sm">Updates will appear here as they happen</p>
          </div>
        ) : (
          notifications.map((notification) => {
            const IconComponent = notification.icon || getSeverityIcon(notification.severity);
            return (
              <div
                key={notification.id}
                className={`p-4 rounded-lg border-l-4 ${getSeverityColor(notification.severity)}`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3">
                    <IconComponent className="h-5 w-5 mt-0.5 flex-shrink-0" />
                    <div className="flex-1">
                      <h4 className="text-sm font-semibold">{notification.title}</h4>
                      <p className="text-sm mt-1">{notification.message}</p>
                      <div className="flex items-center mt-2 space-x-4 text-xs text-gray-500">
                        <span>{notification.projectName}</span>
                        <span>{formatTimeAgo(notification.timestamp)}</span>
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={() => dismissNotification(notification.id)}
                    className="text-gray-400 hover:text-gray-600 flex-shrink-0"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Update Types Info */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="text-sm font-semibold text-blue-800 mb-2">Update Types</h4>
        <div className="grid grid-cols-2 gap-2 text-xs text-blue-700">
          <div className="flex items-center">
            <CheckCircle className="h-3 w-3 mr-1" />
            Status Changes
          </div>
          <div className="flex items-center">
            <DollarSign className="h-3 w-3 mr-1" />
            Budget Updates
          </div>
          <div className="flex items-center">
            <Calendar className="h-3 w-3 mr-1" />
            Timeline Changes
          </div>
          <div className="flex items-center">
            <MapPin className="h-3 w-3 mr-1" />
            Location Updates
          </div>
          <div className="flex items-center">
            <Activity className="h-3 w-3 mr-1" />
            AI Analysis
          </div>
          <div className="flex items-center">
            <AlertTriangle className="h-3 w-3 mr-1" />
            Delay Alerts
          </div>
        </div>
      </div>
    </div>
  );
};

export default RealTimeUpdates;
