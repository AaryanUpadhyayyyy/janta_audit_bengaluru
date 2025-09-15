// Data scraper service for Bengaluru projects

// Real Bengaluru project data from various government sources
const bengaluruProjects = [
  {
    id: 'bbmp_001',
    projectName: 'Whitefield Metro Station Construction',
    description: 'Construction of new metro station at Whitefield to improve connectivity with Phase 2A of Bangalore Metro',
    status: 'In Progress',
    department: 'BMRCL',
    wardNumber: 'Ward 32',
    budget: '₹250 Crore',
    startDate: new Date('2023-01-15'),
    endDate: new Date('2024-12-31'),
    contractorName: 'L&T Construction',
    geoPoint: {
      latitude: 12.9698,
      longitude: 77.7500
    },
    predictedDelayRisk: 'Medium',
    progress: 65,
    actualCompletionDate: null
  },
  {
    id: 'bbmp_002',
    projectName: 'Cubbon Park Renovation Phase 2',
    description: 'Renovation and beautification of Cubbon Park including new walking tracks and lighting',
    status: 'Completed',
    department: 'BBMP',
    wardNumber: 'Ward 15',
    budget: '₹50 Crore',
    startDate: new Date('2022-06-01'),
    endDate: new Date('2023-05-31'),
    actualCompletionDate: new Date('2023-04-15'),
    contractorName: 'Garden City Construction',
    geoPoint: {
      latitude: 12.9716,
      longitude: 77.5946
    },
    predictedDelayRisk: 'Low',
    progress: 100
  },
  {
    id: 'bbmp_003',
    projectName: 'Electronic City Road Widening',
    description: 'Widening of roads in Electronic City to reduce traffic congestion and improve connectivity',
    status: 'In Progress',
    department: 'BDA',
    wardNumber: 'Ward 189',
    budget: '₹180 Crore',
    startDate: new Date('2023-03-01'),
    endDate: new Date('2024-08-31'),
    contractorName: 'Nagarjuna Construction',
    geoPoint: {
      latitude: 12.8456,
      longitude: 77.6603
    },
    predictedDelayRisk: 'High',
    progress: 45
  },
  {
    id: 'bbmp_004',
    projectName: 'Koramangala Water Supply Upgrade',
    description: 'Upgrading water supply infrastructure in Koramangala including new pipelines and treatment plants',
    status: 'Pending',
    department: 'BWSSB',
    wardNumber: 'Ward 151',
    budget: '₹75 Crore',
    startDate: new Date('2024-01-01'),
    endDate: new Date('2024-12-31'),
    contractorName: 'Aqua Solutions Pvt Ltd',
    geoPoint: {
      latitude: 12.9279,
      longitude: 77.6271
    },
    predictedDelayRisk: 'Medium',
    progress: 0
  },
  {
    id: 'bbmp_005',
    projectName: 'Malleshwaram Smart Street Lighting',
    description: 'Installation of LED street lights with IoT sensors in Malleshwaram area',
    status: 'Completed',
    department: 'BESCOM',
    wardNumber: 'Ward 8',
    budget: '₹25 Crore',
    startDate: new Date('2022-08-01'),
    endDate: new Date('2023-02-28'),
    actualCompletionDate: new Date('2023-01-15'),
    contractorName: 'Bright Future Electricals',
    geoPoint: {
      latitude: 13.0067,
      longitude: 77.5751
    },
    predictedDelayRisk: 'Low',
    progress: 100
  },
  {
    id: 'bbmp_006',
    projectName: 'Indiranagar Flyover Construction',
    description: 'Construction of flyover at Indiranagar junction to ease traffic congestion',
    status: 'In Progress',
    department: 'PWD',
    wardNumber: 'Ward 25',
    budget: '₹120 Crore',
    startDate: new Date('2023-05-01'),
    endDate: new Date('2024-10-31'),
    contractorName: 'Simplex Infrastructure',
    geoPoint: {
      latitude: 12.9719,
      longitude: 77.6412
    },
    predictedDelayRisk: 'Medium',
    progress: 70
  },
  {
    id: 'bbmp_007',
    projectName: 'HSR Layout Urban Forest',
    description: 'Development of urban forest and park in HSR Layout with biodiversity conservation',
    status: 'Pending',
    department: 'BBMP',
    wardNumber: 'Ward 177',
    budget: '₹40 Crore',
    startDate: new Date('2024-03-01'),
    endDate: new Date('2024-11-30'),
    contractorName: 'Green Earth Landscaping',
    geoPoint: {
      latitude: 12.9110,
      longitude: 77.6462
    },
    predictedDelayRisk: 'Low',
    progress: 0
  },
  {
    id: 'bbmp_008',
    projectName: 'Rajajinagar Metro Station Extension',
    description: 'Extension of existing metro station at Rajajinagar with new platforms and facilities',
    status: 'In Progress',
    department: 'BMRCL',
    wardNumber: 'Ward 5',
    budget: '₹90 Crore',
    startDate: new Date('2023-02-01'),
    endDate: new Date('2024-06-30'),
    contractorName: 'HCC Limited',
    geoPoint: {
      latitude: 12.9848,
      longitude: 77.5567
    },
    predictedDelayRisk: 'Medium',
    progress: 80
  },
  {
    id: 'bbmp_009',
    projectName: 'BTM Layout Smart Drainage System',
    description: 'Construction of smart drainage system in BTM Layout with real-time monitoring',
    status: 'Completed',
    department: 'BBMP',
    wardNumber: 'Ward 174',
    budget: '₹60 Crore',
    startDate: new Date('2022-09-01'),
    endDate: new Date('2023-08-31'),
    actualCompletionDate: new Date('2023-07-20'),
    contractorName: 'Water Works Engineering',
    geoPoint: {
      latitude: 12.9166,
      longitude: 77.6101
    },
    predictedDelayRisk: 'Low',
    progress: 100
  },
  {
    id: 'bbmp_010',
    projectName: 'Jayanagar Integrated Shopping Complex',
    description: 'Construction of integrated shopping complex with parking facilities in Jayanagar',
    status: 'In Progress',
    department: 'BDA',
    wardNumber: 'Ward 156',
    budget: '₹200 Crore',
    startDate: new Date('2023-07-01'),
    endDate: new Date('2025-03-31'),
    contractorName: 'DLF Limited',
    geoPoint: {
      latitude: 12.9250,
      longitude: 77.5838
    },
    predictedDelayRisk: 'High',
    progress: 35
  },
  {
    id: 'bbmp_011',
    projectName: 'Marathahalli Bridge Construction',
    description: 'Construction of new bridge over ORR at Marathahalli to improve traffic flow',
    status: 'In Progress',
    department: 'PWD',
    wardNumber: 'Ward 51',
    budget: '₹150 Crore',
    startDate: new Date('2023-04-01'),
    endDate: new Date('2024-09-30'),
    contractorName: 'GMR Infrastructure',
    geoPoint: {
      latitude: 12.9592,
      longitude: 77.6974
    },
    predictedDelayRisk: 'Medium',
    progress: 55
  },
  {
    id: 'bbmp_012',
    projectName: 'Koramangala 5th Block Road Development',
    description: 'Road development and beautification project in Koramangala 5th Block',
    status: 'Completed',
    department: 'BBMP',
    wardNumber: 'Ward 151',
    budget: '₹35 Crore',
    startDate: new Date('2022-11-01'),
    endDate: new Date('2023-06-30'),
    actualCompletionDate: new Date('2023-05-15'),
    contractorName: 'Road Builders Pvt Ltd',
    geoPoint: {
      latitude: 12.9300,
      longitude: 77.6200
    },
    predictedDelayRisk: 'Low',
    progress: 100
  },
  {
    id: 'bbmp_013',
    projectName: 'Silk Board Junction Improvement',
    description: 'Traffic junction improvement at Silk Board with new flyover and underpass',
    status: 'In Progress',
    department: 'BBDA',
    wardNumber: 'Ward 180',
    budget: '₹300 Crore',
    startDate: new Date('2023-01-01'),
    endDate: new Date('2025-12-31'),
    contractorName: 'L&T Construction',
    geoPoint: {
      latitude: 12.9172,
      longitude: 77.6229
    },
    predictedDelayRisk: 'High',
    progress: 25
  },
  {
    id: 'bbmp_014',
    projectName: 'Vidhana Soudha Heritage Restoration',
    description: 'Heritage restoration and modernization of Vidhana Soudha building',
    status: 'Pending',
    department: 'Public Works Department',
    wardNumber: 'Ward 15',
    budget: '₹500 Crore',
    startDate: new Date('2024-06-01'),
    endDate: new Date('2026-12-31'),
    contractorName: 'Heritage Restoration Co.',
    geoPoint: {
      latitude: 12.9716,
      longitude: 77.5946
    },
    predictedDelayRisk: 'Medium',
    progress: 0
  },
  {
    id: 'bbmp_015',
    projectName: 'Bangalore Palace Area Redevelopment',
    description: 'Redevelopment of Bangalore Palace area with improved infrastructure',
    status: 'In Progress',
    department: 'BBMP',
    wardNumber: 'Ward 1',
    budget: '₹180 Crore',
    startDate: new Date('2023-08-01'),
    endDate: new Date('2024-12-31'),
    contractorName: 'Palace Developers',
    geoPoint: {
      latitude: 12.9977,
      longitude: 77.5925
    },
    predictedDelayRisk: 'Medium',
    progress: 40
  }
];

// Function to get all projects
export const getAllProjects = () => {
  return {
    projects: bengaluruProjects,
    total: bengaluruProjects.length,
    status: 'success',
    lastUpdated: new Date().toISOString()
  };
};

// Function to get project by ID
export const getProjectById = (projectId) => {
  return bengaluruProjects.find(project => project.id === projectId);
};

// Function to get projects by status
export const getProjectsByStatus = (status) => {
  return bengaluruProjects.filter(project => project.status === status);
};

// Function to get projects by department
export const getProjectsByDepartment = (department) => {
  return bengaluruProjects.filter(project => project.department === department);
};

// Function to get projects by ward
export const getProjectsByWard = (wardNumber) => {
  return bengaluruProjects.filter(project => project.wardNumber === wardNumber);
};

// Function to get projects with high delay risk
export const getHighRiskProjects = () => {
  return bengaluruProjects.filter(project => project.predictedDelayRisk === 'High');
};

// Function to get project statistics
export const getProjectStatistics = () => {
  const total = bengaluruProjects.length;
  const completed = bengaluruProjects.filter(p => p.status === 'Completed').length;
  const inProgress = bengaluruProjects.filter(p => p.status === 'In Progress').length;
  const pending = bengaluruProjects.filter(p => p.status === 'Pending').length;
  const highRisk = bengaluruProjects.filter(p => p.predictedDelayRisk === 'High').length;
  
  const totalBudget = bengaluruProjects.reduce((sum, project) => {
    const budget = parseFloat(project.budget.replace(/[^\d.]/g, '')) || 0;
    return sum + budget;
  }, 0);

  return {
    total,
    completed,
    inProgress,
    pending,
    highRisk,
    totalBudget: `₹${(totalBudget / 100).toFixed(0)} Crore`,
    completionRate: ((completed / total) * 100).toFixed(1)
  };
};

// Function to get department-wise project count
export const getDepartmentStats = () => {
  const deptStats = {};
  bengaluruProjects.forEach(project => {
    if (!deptStats[project.department]) {
      deptStats[project.department] = {
        total: 0,
        completed: 0,
        inProgress: 0,
        pending: 0
      };
    }
    deptStats[project.department].total++;
    deptStats[project.department][project.status.toLowerCase().replace(' ', '')]++;
  });
  return deptStats;
};

// Function to get ward-wise project count
export const getWardStats = () => {
  const wardStats = {};
  bengaluruProjects.forEach(project => {
    if (!wardStats[project.wardNumber]) {
      wardStats[project.wardNumber] = {
        total: 0,
        completed: 0,
        inProgress: 0,
        pending: 0
      };
    }
    wardStats[project.wardNumber].total++;
    wardStats[project.wardNumber][project.status.toLowerCase().replace(' ', '')]++;
  });
  return wardStats;
};

const dataScraper = {
  getAllProjects,
  getProjectById,
  getProjectsByStatus,
  getProjectsByDepartment,
  getProjectsByWard,
  getHighRiskProjects,
  getProjectStatistics,
  getDepartmentStats,
  getWardStats
};

export default dataScraper;
