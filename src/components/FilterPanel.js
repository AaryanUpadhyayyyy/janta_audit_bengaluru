import React, { useState, useEffect } from 'react';
import { X, MapPin, Building, DollarSign, Search, Calendar, Filter } from 'lucide-react';

const FilterPanel = ({ filters, onFiltersChange, projects = [] }) => {
  const bengaluruWards = [
    'Ward 1', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6', 'Ward 7', 'Ward 8',
    'Ward 9', 'Ward 10', 'Ward 11', 'Ward 12', 'Ward 13', 'Ward 14', 'Ward 15', 'Ward 16',
    'Ward 17', 'Ward 18', 'Ward 19', 'Ward 20', 'Ward 21', 'Ward 22', 'Ward 23', 'Ward 24',
    'Ward 25', 'Ward 26', 'Ward 27', 'Ward 28', 'Ward 29', 'Ward 30', 'Ward 31', 'Ward 32',
    'Ward 33', 'Ward 34', 'Ward 35', 'Ward 36', 'Ward 37', 'Ward 38', 'Ward 39', 'Ward 40',
    'Ward 41', 'Ward 42', 'Ward 43', 'Ward 44', 'Ward 45', 'Ward 46', 'Ward 47', 'Ward 48',
    'Ward 49', 'Ward 50', 'Ward 51', 'Ward 52', 'Ward 53', 'Ward 54', 'Ward 55', 'Ward 56',
    'Ward 57', 'Ward 58', 'Ward 59', 'Ward 60', 'Ward 61', 'Ward 62', 'Ward 63', 'Ward 64',
    'Ward 65', 'Ward 66', 'Ward 67', 'Ward 68', 'Ward 69', 'Ward 70', 'Ward 71', 'Ward 72',
    'Ward 73', 'Ward 74', 'Ward 75', 'Ward 76', 'Ward 77', 'Ward 78', 'Ward 79', 'Ward 80',
    'Ward 81', 'Ward 82', 'Ward 83', 'Ward 84', 'Ward 85', 'Ward 86', 'Ward 87', 'Ward 88',
    'Ward 89', 'Ward 90', 'Ward 91', 'Ward 92', 'Ward 93', 'Ward 94', 'Ward 95', 'Ward 96',
    'Ward 97', 'Ward 98', 'Ward 99', 'Ward 100', 'Ward 101', 'Ward 102', 'Ward 103', 'Ward 104',
    'Ward 105', 'Ward 106', 'Ward 107', 'Ward 108', 'Ward 109', 'Ward 110', 'Ward 111', 'Ward 112',
    'Ward 113', 'Ward 114', 'Ward 115', 'Ward 116', 'Ward 117', 'Ward 118', 'Ward 119', 'Ward 120',
    'Ward 121', 'Ward 122', 'Ward 123', 'Ward 124', 'Ward 125', 'Ward 126', 'Ward 127', 'Ward 128',
    'Ward 129', 'Ward 130', 'Ward 131', 'Ward 132', 'Ward 133', 'Ward 134', 'Ward 135', 'Ward 136',
    'Ward 137', 'Ward 138', 'Ward 139', 'Ward 140', 'Ward 141', 'Ward 142', 'Ward 143', 'Ward 144',
    'Ward 145', 'Ward 146', 'Ward 147', 'Ward 148', 'Ward 149', 'Ward 150', 'Ward 151', 'Ward 152',
    'Ward 153', 'Ward 154', 'Ward 155', 'Ward 156', 'Ward 157', 'Ward 158', 'Ward 159', 'Ward 160',
    'Ward 161', 'Ward 162', 'Ward 163', 'Ward 164', 'Ward 165', 'Ward 166', 'Ward 167', 'Ward 168',
    'Ward 169', 'Ward 170', 'Ward 171', 'Ward 172', 'Ward 173', 'Ward 174', 'Ward 175', 'Ward 176',
    'Ward 177', 'Ward 178', 'Ward 179', 'Ward 180', 'Ward 181', 'Ward 182', 'Ward 183', 'Ward 184',
    'Ward 185', 'Ward 186', 'Ward 187', 'Ward 188', 'Ward 189', 'Ward 190', 'Ward 191', 'Ward 192',
    'Ward 193', 'Ward 194', 'Ward 195', 'Ward 196', 'Ward 197', 'Ward 198', 'Ward 199', 'Ward 200'
  ];

  const [departments, setDepartments] = useState([]);
  const [statuses, setStatuses] = useState([]);

  const budgetRanges = [
    { label: 'All Budgets', value: 'all' },
    { label: 'Under ₹10 Lakh', value: 'low' },
    { label: '₹10 Lakh - ₹1 Crore', value: 'medium' },
    { label: '₹1 Crore - ₹10 Crore', value: 'high' },
    { label: 'Above ₹10 Crore', value: 'very-high' }
  ];

  const dateRanges = [
    { label: 'All Time', value: 'all' },
    { label: 'Last Month', value: 'last-month' },
    { label: 'Last 3 Months', value: 'last-3-months' },
    { label: 'Last 6 Months', value: 'last-6-months' },
    { label: 'Last Year', value: 'last-year' }
  ];

  // Extract unique departments and statuses from projects
  useEffect(() => {
    if (projects.length > 0) {
      const uniqueDepartments = [...new Set(projects.map(p => p.department).filter(Boolean))];
      const uniqueStatuses = [...new Set(projects.map(p => p.status).filter(Boolean))];
      
      setDepartments(uniqueDepartments);
      setStatuses(uniqueStatuses);
    }
  }, [projects]);

  const handleFilterChange = (filterType, value) => {
    onFiltersChange(prev => ({ ...prev, [filterType]: value }));
  };

  const clearFilters = () => {
    onFiltersChange({
      status: 'all',
      department: 'all',
      budgetRange: 'all',
      dateRange: 'all',
      searchQuery: ''
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 w-full">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold text-gray-900 flex items-center">
          <Filter className="h-5 w-5 mr-2" />
          Filter Projects
        </h3>
      </div>

      {/* Search Query */}
      <div className="mb-4">
        <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
          <Search className="h-4 w-4 mr-2" />
          Search Projects
        </label>
        <input
          type="text"
          value={filters.searchQuery || ''}
          onChange={(e) => handleFilterChange('searchQuery', e.target.value)}
          placeholder="Search by name, description, contractor..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {/* Status Filter */}
      <div className="mb-4">
        <label className="text-sm font-medium text-gray-700 mb-2 block">
          Project Status
        </label>
        <select
          value={filters.status || 'all'}
          onChange={(e) => handleFilterChange('status', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="all">All Statuses</option>
          {statuses.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      </div>

      {/* Department Filter */}
      <div className="mb-4">
        <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
          <Building className="h-4 w-4 mr-2" />
          Department
        </label>
        <select
          value={filters.department || 'all'}
          onChange={(e) => handleFilterChange('department', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="all">All Departments</option>
          {departments.map((dept) => (
            <option key={dept} value={dept}>
              {dept}
            </option>
          ))}
        </select>
      </div>

      {/* Budget Range Filter */}
      <div className="mb-4">
        <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
          <DollarSign className="h-4 w-4 mr-2" />
          Budget Range
        </label>
        <select
          value={filters.budgetRange || 'all'}
          onChange={(e) => handleFilterChange('budgetRange', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {budgetRanges.map((range) => (
            <option key={range.value} value={range.value}>
              {range.label}
            </option>
          ))}
        </select>
      </div>

      {/* Date Range Filter */}
      <div className="mb-4">
        <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
          <Calendar className="h-4 w-4 mr-2" />
          Date Range
        </label>
        <select
          value={filters.dateRange || 'all'}
          onChange={(e) => handleFilterChange('dateRange', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {dateRanges.map((range) => (
            <option key={range.value} value={range.value}>
              {range.label}
            </option>
          ))}
        </select>
      </div>

      {/* Clear Filters Button */}
      <button
        onClick={clearFilters}
        className="w-full bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 transition-colors"
      >
        Clear All Filters
      </button>
    </div>
  );
};

export default FilterPanel;
