// Mock project data for Bengaluru
export const mockProjects = [
  {
    id: '1',
    projectName: 'Whitefield Metro Station Construction',
    description: 'Construction of new metro station at Whitefield to improve connectivity',
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
    predictedDelayRisk: 'Medium'
  },
  {
    id: '2',
    projectName: 'Cubbon Park Renovation',
    description: 'Renovation and beautification of Cubbon Park',
    status: 'Completed',
    department: 'BBMP',
    wardNumber: 'Ward 15',
    budget: '₹50 Crore',
    startDate: new Date('2022-06-01'),
    endDate: new Date('2023-05-31'),
    contractorName: 'Garden City Construction',
    geoPoint: {
      latitude: 12.9716,
      longitude: 77.5946
    },
    predictedDelayRisk: 'Low'
  },
  {
    id: '3',
    projectName: 'Electronic City Road Widening',
    description: 'Widening of roads in Electronic City to reduce traffic congestion',
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
    predictedDelayRisk: 'High'
  },
  {
    id: '4',
    projectName: 'Koramangala Water Supply Upgrade',
    description: 'Upgrading water supply infrastructure in Koramangala',
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
    predictedDelayRisk: 'Medium'
  },
  {
    id: '5',
    projectName: 'Malleshwaram Street Lighting',
    description: 'Installation of LED street lights in Malleshwaram area',
    status: 'Completed',
    department: 'BESCOM',
    wardNumber: 'Ward 8',
    budget: '₹25 Crore',
    startDate: new Date('2022-08-01'),
    endDate: new Date('2023-02-28'),
    contractorName: 'Bright Future Electricals',
    geoPoint: {
      latitude: 13.0067,
      longitude: 77.5751
    },
    predictedDelayRisk: 'Low'
  },
  {
    id: '6',
    projectName: 'Indiranagar Flyover Construction',
    description: 'Construction of flyover at Indiranagar junction',
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
    predictedDelayRisk: 'Medium'
  },
  {
    id: '7',
    projectName: 'HSR Layout Park Development',
    description: 'Development of new park in HSR Layout',
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
    predictedDelayRisk: 'Low'
  },
  {
    id: '8',
    projectName: 'Rajajinagar Metro Station Extension',
    description: 'Extension of existing metro station at Rajajinagar',
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
    predictedDelayRisk: 'Medium'
  },
  {
    id: '9',
    projectName: 'BTM Layout Drainage System',
    description: 'Construction of new drainage system in BTM Layout',
    status: 'Completed',
    department: 'BBMP',
    wardNumber: 'Ward 174',
    budget: '₹60 Crore',
    startDate: new Date('2022-09-01'),
    endDate: new Date('2023-08-31'),
    contractorName: 'Water Works Engineering',
    geoPoint: {
      latitude: 12.9166,
      longitude: 77.6101
    },
    predictedDelayRisk: 'Low'
  },
  {
    id: '10',
    projectName: 'Jayanagar Shopping Complex',
    description: 'Construction of new shopping complex in Jayanagar',
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
    predictedDelayRisk: 'High'
  }
];

export const mockProjectResponse = {
  projects: mockProjects,
  total: mockProjects.length,
  status: 'success'
};
