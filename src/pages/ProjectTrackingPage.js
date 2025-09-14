import React, { useState, useEffect } from 'react';
import ProjectTracking from '../components/ProjectTracking';
import ProjectDashboard from '../components/ProjectDashboard';
import ProjectDataManager from '../components/ProjectDataManager';
import RealTimeUpdates from '../components/RealTimeUpdates';
import { 
  BarChart3, 
  Map, 
  Settings, 
  Bell, 
  Database,
  Activity
} from 'lucide-react';

const ProjectTrackingPage = () => {
  const [activeTab, setActiveTab] = useState('tracking');
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [notifications, setNotifications] = useState([]);

  // Load projects on component mount
  useEffect(() => {
    loadProjects();
  }, []);

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

  const handleProjectCreate = async (projectData) => {
    try {
      const response = await fetch('/api/submit-project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(projectData)
      });

      if (!response.ok) {
        throw new Error('Failed to create project');
      }

      const result = await response.json();
      
      // Add the new project to the list
      const newProject = {
        id: result.projectId,
        ...projectData,
        timestamp: new Date().toISOString()
      };
      
      setProjects(prev => [newProject, ...prev]);
      
      // Add notification
      addNotification({
        type: 'project_created',
        title: 'Project Created',
        message: `Project "${projectData.projectName}" has been created successfully`,
        severity: 'success'
      });

    } catch (error) {
      console.error('Error creating project:', error);
      throw error;
    }
  };

  const handleProjectUpdate = async (projectId, projectData) => {
    try {
      const response = await fetch(`/api/projects/${projectId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(projectData)
      });

      if (!response.ok) {
        throw new Error('Failed to update project');
      }

      // Update the project in the list
      setProjects(prev => 
        prev.map(project => 
          project.id === projectId 
            ? { ...project, ...projectData, lastUpdated: new Date().toISOString() }
            : project
        )
      );

      // Add notification
      addNotification({
        type: 'project_updated',
        title: 'Project Updated',
        message: `Project "${projectData.projectName}" has been updated successfully`,
        severity: 'info'
      });

    } catch (error) {
      console.error('Error updating project:', error);
      throw error;
    }
  };

  const handleProjectDelete = async (projectId) => {
    try {
      const response = await fetch(`/api/projects/${projectId}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        throw new Error('Failed to delete project');
      }

      // Remove the project from the list
      setProjects(prev => prev.filter(project => project.id !== projectId));

      // Add notification
      addNotification({
        type: 'project_deleted',
        title: 'Project Deleted',
        message: 'Project has been deleted successfully',
        severity: 'warning'
      });

    } catch (error) {
      console.error('Error deleting project:', error);
      throw error;
    }
  };

  const handleProjectUpdateFromTracking = (updates) => {
    // Handle updates from the tracking component
    updates.forEach(update => {
      if (update.type === 'project_updated') {
        setProjects(prev => 
          prev.map(project => 
            project.id === update.projectId 
              ? { ...project, ...update.data, lastUpdated: new Date().toISOString() }
              : project
          )
        );
      }
    });
  };

  const addNotification = (notification) => {
    const newNotification = {
      id: `notif_${Date.now()}_${Math.random()}`,
      timestamp: new Date(),
      ...notification
    };
    setNotifications(prev => [newNotification, ...prev].slice(0, 100)); // Keep last 100 notifications
  };

  const tabs = [
    {
      id: 'tracking',
      name: 'Project Tracking',
      icon: Map,
      description: 'Interactive map view with project locations and AI analysis'
    },
    {
      id: 'dashboard',
      name: 'Analytics Dashboard',
      icon: BarChart3,
      description: 'Comprehensive analytics and performance metrics'
    },
    {
      id: 'management',
      name: 'Data Management',
      icon: Database,
      description: 'Create, edit, and manage project data'
    },
    {
      id: 'updates',
      name: 'Real-Time Updates',
      icon: Bell,
      description: 'Live notifications and project updates'
    }
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading project tracking system...</p>
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
      <div className="bg-white border-b border-gray-200">
        <div className="px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Project Tracking System</h1>
          <p className="text-gray-600">AI-powered project monitoring and analysis using free APIs</p>
        </div>
        
        {/* Tab Navigation */}
        <div className="px-6">
          <nav className="flex space-x-8">
            {tabs.map((tab) => {
              const IconComponent = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center px-1 py-4 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <IconComponent className="h-5 w-5 mr-2" />
                  {tab.name}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'tracking' && (
          <ProjectTracking 
            projects={projects}
            onProjectUpdate={handleProjectUpdateFromTracking}
          />
        )}

        {activeTab === 'dashboard' && (
          <ProjectDashboard projects={projects} />
        )}

        {activeTab === 'management' && (
          <div className="p-6">
            <ProjectDataManager
              projects={projects}
              onProjectCreate={handleProjectCreate}
              onProjectUpdate={handleProjectUpdate}
              onProjectDelete={handleProjectDelete}
            />
          </div>
        )}

        {activeTab === 'updates' && (
          <div className="p-6">
            <RealTimeUpdates
              projects={projects}
              onProjectUpdate={handleProjectUpdateFromTracking}
            />
          </div>
        )}
      </div>

      {/* Notifications Toast */}
      {notifications.length > 0 && (
        <div className="fixed top-4 right-4 z-50 space-y-2">
          {notifications.slice(0, 3).map((notification) => (
            <div
              key={notification.id}
              className={`p-4 rounded-lg shadow-lg border-l-4 ${
                notification.severity === 'success' ? 'bg-green-50 border-green-400 text-green-800' :
                notification.severity === 'warning' ? 'bg-yellow-50 border-yellow-400 text-yellow-800' :
                notification.severity === 'error' ? 'bg-red-50 border-red-400 text-red-800' :
                'bg-blue-50 border-blue-400 text-blue-800'
              }`}
            >
              <div className="flex items-center">
                <Activity className="h-5 w-5 mr-2" />
                <div>
                  <p className="font-semibold">{notification.title}</p>
                  <p className="text-sm">{notification.message}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Footer */}
      <div className="bg-gray-50 border-t border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between text-sm text-gray-600">
          <div className="flex items-center space-x-4">
            <span>Total Projects: {projects.length}</span>
            <span>•</span>
            <span>Last Updated: {new Date().toLocaleString()}</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>System Online</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectTrackingPage;
