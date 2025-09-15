import React, { useState, useEffect, useCallback } from 'react';
import { 
  DollarSign, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  BarChart3
} from 'lucide-react';

const ProjectDashboard = ({ projects = [] }) => {
  const [selectedTimeRange, setSelectedTimeRange] = useState('6months');
  const [selectedDepartment, setSelectedDepartment] = useState('all');
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    if (projects.length > 0) {
      calculateDashboardData();
    }
  }, [projects, selectedTimeRange, selectedDepartment, calculateDashboardData]);

  const calculateDashboardData = useCallback(() => {
    const now = new Date();
    const timeRanges = {
      '1month': 30,
      '3months': 90,
      '6months': 180,
      '1year': 365,
      'all': Infinity
    };
    
    const days = timeRanges[selectedTimeRange];
    const cutoffDate = days === Infinity ? new Date(0) : new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
    
    let filteredProjects = projects.filter(project => {
      const projectDate = new Date(project.startDate || project.timestamp);
      return projectDate >= cutoffDate;
    });

    if (selectedDepartment !== 'all') {
      filteredProjects = filteredProjects.filter(project => project.department === selectedDepartment);
    }

    const stats = {
      total: filteredProjects.length,
      completed: filteredProjects.filter(p => p.status === 'Completed').length,
      inProgress: filteredProjects.filter(p => p.status === 'In Progress').length,
      pending: filteredProjects.filter(p => p.status === 'Pending').length,
      cancelled: filteredProjects.filter(p => p.status === 'Cancelled').length,
      delayed: filteredProjects.filter(p => p.status === 'Delayed').length,
    };

    const budgetStats = calculateBudgetStats(filteredProjects);
    const timelineStats = calculateTimelineStats(filteredProjects);
    const departmentStats = calculateDepartmentStats(filteredProjects);
    const locationStats = calculateLocationStats(filteredProjects);
    const performanceMetrics = calculatePerformanceMetrics(filteredProjects);

    setDashboardData({
      stats,
      budgetStats,
      timelineStats,
      departmentStats,
      locationStats,
      performanceMetrics,
      filteredProjects
    });
  }, [projects, selectedTimeRange, selectedDepartment]);

  const calculateBudgetStats = (projects) => {
    const budgets = projects.map(p => extractBudgetNumeric(p.budget)).filter(b => b > 0);
    
    return {
      total: budgets.reduce((sum, b) => sum + b, 0),
      average: budgets.length > 0 ? budgets.reduce((sum, b) => sum + b, 0) / budgets.length : 0,
      median: budgets.length > 0 ? budgets.sort((a, b) => a - b)[Math.floor(budgets.length / 2)] : 0,
      min: budgets.length > 0 ? Math.min(...budgets) : 0,
      max: budgets.length > 0 ? Math.max(...budgets) : 0,
      distribution: {
        under1Lakh: budgets.filter(b => b < 100000).length,
        '1Lakh-10Lakh': budgets.filter(b => b >= 100000 && b < 1000000).length,
        '10Lakh-1Crore': budgets.filter(b => b >= 1000000 && b < 10000000).length,
        '1Crore-10Crore': budgets.filter(b => b >= 10000000 && b < 100000000).length,
        above10Crore: budgets.filter(b => b >= 100000000).length
      }
    };
  };

  const calculateTimelineStats = (projects) => {
    const now = new Date();
    const projectsWithDuration = projects.filter(p => p.startDate && p.endDate);
    
    const durations = projectsWithDuration.map(p => {
      const start = new Date(p.startDate);
      const end = new Date(p.endDate);
      return Math.ceil((end - start) / (1000 * 60 * 60 * 24)); // days
    });

    const overdueProjects = projects.filter(p => {
      if (!p.endDate || p.status === 'Completed') return false;
      return new Date(p.endDate) < now;
    });

    return {
      averageDuration: durations.length > 0 ? durations.reduce((sum, d) => sum + d, 0) / durations.length : 0,
      overdueCount: overdueProjects.length,
      overduePercentage: projects.length > 0 ? (overdueProjects.length / projects.length) * 100 : 0,
      completionRate: projects.length > 0 ? (projects.filter(p => p.status === 'Completed').length / projects.length) * 100 : 0
    };
  };

  const calculateDepartmentStats = (projects) => {
    const deptCounts = {};
    projects.forEach(p => {
      if (p.department) {
        deptCounts[p.department] = (deptCounts[p.department] || 0) + 1;
      }
    });

    return Object.entries(deptCounts)
      .map(([dept, count]) => ({ department: dept, count, percentage: (count / projects.length) * 100 }))
      .sort((a, b) => b.count - a.count);
  };

  const calculateLocationStats = (projects) => {
    const locations = {};
    projects.forEach(p => {
      if (p.geoPoint) {
        const key = `${p.geoPoint.latitude.toFixed(2)},${p.geoPoint.longitude.toFixed(2)}`;
        locations[key] = (locations[key] || 0) + 1;
      }
    });

    return Object.entries(locations)
      .map(([location, count]) => ({ location, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10); // Top 10 locations
  };

  const calculatePerformanceMetrics = (projects) => {
    const projectsWithAnalysis = projects.filter(p => p.satelliteAnalysis);
    const statusMismatches = projectsWithAnalysis.filter(p => 
      p.satelliteAnalysis?.project_status?.mismatch
    ).length;

    const avgConfidence = projectsWithAnalysis.length > 0 
      ? projectsWithAnalysis.reduce((sum, p) => sum + (p.satelliteAnalysis?.confidence_score || 0), 0) / projectsWithAnalysis.length
      : 0;

    return {
      analyzedProjects: projectsWithAnalysis.length,
      analysisPercentage: projects.length > 0 ? (projectsWithAnalysis.length / projects.length) * 100 : 0,
      statusMismatches,
      mismatchPercentage: projectsWithAnalysis.length > 0 ? (statusMismatches / projectsWithAnalysis.length) * 100 : 0,
      averageConfidence: avgConfidence * 100,
      highConfidenceProjects: projectsWithAnalysis.filter(p => (p.satelliteAnalysis?.confidence_score || 0) > 0.8).length
    };
  };

  const extractBudgetNumeric = (budgetStr) => {
    if (!budgetStr) return 0;
    
    const str = String(budgetStr).replace(/,/g, '').replace(/₹/g, '').replace(/Rs\./g, '');
    
    let multiplier = 1;
    if (str.includes('Lakh') || str.includes('L')) {
      multiplier = 100000;
    } else if (str.includes('Crore') || str.includes('Cr')) {
      multiplier = 10000000;
    }
    
    const numbers = str.match(/[\d.]+/);
    return numbers ? parseFloat(numbers[0]) * multiplier : 0;
  };

  const formatCurrency = (amount) => {
    if (amount >= 10000000) {
      return `₹${(amount / 10000000).toFixed(1)}Cr`;
    } else if (amount >= 100000) {
      return `₹${(amount / 100000).toFixed(1)}L`;
    } else {
      return `₹${amount.toLocaleString()}`;
    }
  };

  if (!dashboardData) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-full p-6 bg-gray-50">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Project Dashboard</h1>
        <p className="text-gray-600">Comprehensive analytics and insights for project tracking</p>
      </div>

      {/* Controls */}
      <div className="mb-6 flex flex-wrap gap-4">
        <div className="flex items-center space-x-2">
          <label className="text-sm font-medium text-gray-700">Time Range:</label>
          <select
            value={selectedTimeRange}
            onChange={(e) => setSelectedTimeRange(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="1month">Last Month</option>
            <option value="3months">Last 3 Months</option>
            <option value="6months">Last 6 Months</option>
            <option value="1year">Last Year</option>
            <option value="all">All Time</option>
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <label className="text-sm font-medium text-gray-700">Department:</label>
          <select
            value={selectedDepartment}
            onChange={(e) => setSelectedDepartment(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Departments</option>
            {dashboardData.departmentStats.map(dept => (
              <option key={dept.department} value={dept.department}>
                {dept.department} ({dept.count})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BarChart3 className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Total Projects</p>
              <p className="text-2xl font-bold text-gray-900">{dashboardData.stats.total}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-gray-900">{dashboardData.stats.completed}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Clock className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">In Progress</p>
              <p className="text-2xl font-bold text-gray-900">{dashboardData.stats.inProgress}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-orange-100 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Delayed</p>
              <p className="text-2xl font-bold text-gray-900">{dashboardData.stats.delayed}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Total Budget</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(dashboardData.budgetStats.total)}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-indigo-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-indigo-600" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Completion Rate</p>
              <p className="text-2xl font-bold text-gray-900">{dashboardData.timelineStats.completionRate.toFixed(1)}%</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts and Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Status Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Project Status Distribution</h3>
          <div className="space-y-3">
            {[
              { status: 'Completed', count: dashboardData.stats.completed, color: 'bg-green-500' },
              { status: 'In Progress', count: dashboardData.stats.inProgress, color: 'bg-blue-500' },
              { status: 'Pending', count: dashboardData.stats.pending, color: 'bg-yellow-500' },
              { status: 'Delayed', count: dashboardData.stats.delayed, color: 'bg-orange-500' },
              { status: 'Cancelled', count: dashboardData.stats.cancelled, color: 'bg-red-500' }
            ].map(({ status, count, color }) => {
              const percentage = dashboardData.stats.total > 0 ? (count / dashboardData.stats.total) * 100 : 0;
              return (
                <div key={status} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full ${color} mr-3`}></div>
                    <span className="text-sm font-medium text-gray-700">{status}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-600">{count}</span>
                    <div className="w-20 bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${color}`}
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-600 w-10 text-right">{percentage.toFixed(1)}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Department Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Projects by Department</h3>
          <div className="space-y-3">
            {dashboardData.departmentStats.slice(0, 5).map(({ department, count, percentage }) => (
              <div key={department} className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700 truncate">{department}</span>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600">{count}</span>
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div 
                      className="h-2 rounded-full bg-blue-500"
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                  <span className="text-sm text-gray-600 w-10 text-right">{percentage.toFixed(1)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Budget Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Budget Distribution</h3>
          <div className="space-y-3">
            {[
              { range: 'Under ₹1L', count: dashboardData.budgetStats.distribution.under1Lakh, color: 'bg-green-500' },
              { range: '₹1L - ₹10L', count: dashboardData.budgetStats.distribution['1Lakh-10Lakh'], color: 'bg-blue-500' },
              { range: '₹10L - ₹1Cr', count: dashboardData.budgetStats.distribution['10Lakh-1Crore'], color: 'bg-yellow-500' },
              { range: '₹1Cr - ₹10Cr', count: dashboardData.budgetStats.distribution['1Crore-10Crore'], color: 'bg-orange-500' },
              { range: 'Above ₹10Cr', count: dashboardData.budgetStats.distribution.above10Crore, color: 'bg-red-500' }
            ].map(({ range, count, color }) => {
              const percentage = dashboardData.stats.total > 0 ? (count / dashboardData.stats.total) * 100 : 0;
              return (
                <div key={range} className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">{range}</span>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-600">{count}</span>
                    <div className="w-20 bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${color}`}
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-600 w-10 text-right">{percentage.toFixed(1)}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Budget Statistics</h3>
          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Total Budget</span>
              <span className="text-sm font-semibold text-gray-900">{formatCurrency(dashboardData.budgetStats.total)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Average Budget</span>
              <span className="text-sm font-semibold text-gray-900">{formatCurrency(dashboardData.budgetStats.average)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Median Budget</span>
              <span className="text-sm font-semibold text-gray-900">{formatCurrency(dashboardData.budgetStats.median)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Highest Budget</span>
              <span className="text-sm font-semibold text-gray-900">{formatCurrency(dashboardData.budgetStats.max)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Lowest Budget</span>
              <span className="text-sm font-semibold text-gray-900">{formatCurrency(dashboardData.budgetStats.min)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">AI Analysis Performance</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{dashboardData.performanceMetrics.analyzedProjects}</div>
            <div className="text-sm text-gray-600">Projects Analyzed</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{dashboardData.performanceMetrics.analysisPercentage.toFixed(1)}%</div>
            <div className="text-sm text-gray-600">Analysis Coverage</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">{dashboardData.performanceMetrics.statusMismatches}</div>
            <div className="text-sm text-gray-600">Status Mismatches</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">{dashboardData.performanceMetrics.averageConfidence.toFixed(1)}%</div>
            <div className="text-sm text-gray-600">Avg Confidence</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectDashboard;
