import React, { createContext, useContext, useState, useEffect } from 'react';
// Firebase imports removed as they're not currently used
// import { 
//   collection, 
//   query, 
//   where, 
//   orderBy, 
//   onSnapshot, 
//   doc, 
//   getDoc,
//   addDoc,
//   serverTimestamp
// } from 'firebase/firestore';
// import { db } from '../firebase/config';
import { fetchProjects, fetchProject, submitProject, submitFeedback, fetchProjectFeedback } from '../services/api';

const ProjectContext = createContext();

export function useProjects() {
  return useContext(ProjectContext);
}

export function ProjectProvider({ children }) {
  const [projects, setProjects] = useState([]);
  const [filteredProjects, setFilteredProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    wardNumber: '',
    department: '',
    status: '',
    budgetRange: ''
  });

  useEffect(() => {
    // Fetch projects from Express.js API
    const loadProjects = async () => {
      try {
        setLoading(true);
        const response = await fetchProjects();
        console.log('Projects loaded:', response);
        setProjects(response.projects || []);
        setFilteredProjects(response.projects || []);
      } catch (error) {
        console.error('Error loading projects:', error);
        setProjects([]);
        setFilteredProjects([]);
      } finally {
        setLoading(false);
      }
    };

    loadProjects();
  }, []);

  useEffect(() => {
    // Apply filters
    let filtered = [...projects];

    if (filters.wardNumber) {
      filtered = filtered.filter(project => project.wardNumber === filters.wardNumber);
    }

    if (filters.department) {
      filtered = filtered.filter(project => project.department === filters.department);
    }

    if (filters.status) {
      filtered = filtered.filter(project => project.status === filters.status);
    }

    if (filters.budgetRange) {
      const [min, max] = filters.budgetRange.split('-').map(Number);
      filtered = filtered.filter(project => {
        const budget = parseFloat(project.budget?.replace(/[^\d.]/g, '') || 0);
        return budget >= min && budget <= max;
      });
    }

    setFilteredProjects(filtered);
  }, [projects, filters]);

  const updateFilters = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const getProjectById = async (projectId) => {
    try {
      return await fetchProject(projectId);
    } catch (error) {
      console.error('Error fetching project:', error);
      throw error;
    }
  };

  const getProjectFeedback = async (projectId) => {
    try {
      const response = await fetchProjectFeedback(projectId);
      return response.feedback || [];
    } catch (error) {
      console.error('Error fetching feedback:', error);
      throw error;
    }
  };

  const submitProjectFeedback = async (projectId, feedbackData) => {
    try {
      return await submitFeedback(
        projectId,
        feedbackData.feedback,
        feedbackData.rating,
        feedbackData.location,
        feedbackData.userId
      );
    } catch (error) {
      console.error('Error submitting feedback:', error);
      throw error;
    }
  };

  const submitNewProject = async (projectData) => {
    try {
      return await submitProject(projectData);
    } catch (error) {
      console.error('Error submitting project:', error);
      throw error;
    }
  };

  const getWardProjects = async (wardNumber) => {
    try {
      // Filter projects by ward number on the client side
      return projects.filter(project => project.wardNumber === wardNumber);
    } catch (error) {
      console.error('Error fetching ward projects:', error);
      throw error;
    }
  };

  const value = {
    projects,
    filteredProjects,
    loading,
    filters,
    updateFilters,
    getProjectById,
    getProjectFeedback,
    submitProjectFeedback,
    submitNewProject,
    getWardProjects
  };

  return (
    <ProjectContext.Provider value={value}>
      {children}
    </ProjectContext.Provider>
  );
}
