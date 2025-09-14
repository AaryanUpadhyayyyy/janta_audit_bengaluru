import React from 'react';
import { Link } from 'react-router-dom';
import { MapPin, Calendar, DollarSign, AlertTriangle, ExternalLink } from 'lucide-react';

const ProjectCard = ({ project, onClick }) => {
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
        return 'text-red-600';
      case 'Medium':
        return 'text-yellow-600';
      case 'Low':
        return 'text-green-600';
      default:
        return 'text-gray-600';
    }
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return 'N/A';
    const date = timestamp.toDate ? timestamp.toDate() : new Date(timestamp);
    return date.toLocaleDateString('en-IN');
  };

  const formatBudget = (budget) => {
    if (!budget) return 'N/A';
    const num = parseFloat(budget.replace(/[^\d.]/g, ''));
    if (num >= 10000000) {
      return `₹${(num / 10000000).toFixed(1)} Cr`;
    } else if (num >= 100000) {
      return `₹${(num / 100000).toFixed(1)} L`;
    } else {
      return `₹${num.toLocaleString('en-IN')}`;
    }
  };

  return (
    <div className="project-card">
      <div className="flex justify-between items-start mb-2">
        <Link
          to={`/project/${project.id}`}
          className="font-semibold text-gray-900 text-sm line-clamp-2 hover:text-blue-600 transition-colors"
        >
          {project.projectName}
        </Link>
        <div className="flex items-center space-x-2">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
            {project.status}
          </span>
          <Link
            to={`/project/${project.id}`}
            className="p-1 hover:bg-gray-100 rounded transition-colors"
            onClick={(e) => e.stopPropagation()}
          >
            <ExternalLink className="h-3 w-3 text-gray-400" />
          </Link>
        </div>
      </div>

      <p className="text-gray-600 text-xs mb-3 line-clamp-2">
        {project.description}
      </p>

      <div className="space-y-2">
        <div className="flex items-center text-xs text-gray-500">
          <MapPin className="h-3 w-3 mr-1" />
          <span>{project.wardNumber}</span>
          <span className="mx-1">•</span>
          <span>{project.department}</span>
        </div>

        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center text-gray-500">
            <Calendar className="h-3 w-3 mr-1" />
            <span>{formatDate(project.startDate)}</span>
          </div>
          <div className="flex items-center text-gray-500">
            <DollarSign className="h-3 w-3 mr-1" />
            <span>{formatBudget(project.budget)}</span>
          </div>
        </div>

        {project.predictedDelayRisk && (
          <div className="flex items-center text-xs">
            <AlertTriangle className="h-3 w-3 mr-1" />
            <span className={`font-medium ${getRiskColor(project.predictedDelayRisk)}`}>
              Delay Risk: {project.predictedDelayRisk}
            </span>
          </div>
        )}

        {project.contractorName && (
          <div className="text-xs text-gray-500">
            Contractor: {project.contractorName}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectCard;
