// Global variables
let map;
let markers = [];
let projects = [];
let filteredProjects = [];
let currentUser = null;

// Initialize Firebase (config is loaded from firebase-config.js)
let app, auth, db;
try {
    if (typeof firebaseConfig !== 'undefined') {
        app = firebase.initializeApp(firebaseConfig);
        auth = firebase.auth();
        db = firebase.firestore();
        console.log('Firebase initialized successfully');
    } else {
        console.warn('Firebase config not found. Please update firebase-config.js');
    }
} catch (error) {
    console.error('Firebase initialization error:', error);
}

// Sample project data
const sampleProjects = [
    {
        id: 1,
        projectName: "Road Widening - MG Road",
        description: "Widening of MG Road from Trinity Circle to Brigade Road",
        wardNumber: "Ward 1",
        department: "BBMP",
        status: "In Progress",
        budget: "₹50,00,000",
        location: { lat: 12.9716, lng: 77.5946 },
        startDate: "2024-01-15",
        endDate: "2024-06-30",
        predictedDelayRisk: "Medium"
    },
    {
        id: 2,
        projectName: "Metro Station Construction",
        description: "New metro station at Whitefield",
        wardNumber: "Ward 2",
        department: "BMRCL",
        status: "Completed",
        budget: "₹2,50,00,000",
        location: { lat: 12.9698, lng: 77.7500 },
        startDate: "2023-06-01",
        endDate: "2024-01-15",
        predictedDelayRisk: "Low"
    },
    {
        id: 3,
        projectName: "Water Pipeline Installation",
        description: "New water pipeline for HSR Layout",
        wardNumber: "Ward 3",
        department: "BWSSB",
        status: "Pending",
        budget: "₹75,00,000",
        location: { lat: 12.9116, lng: 77.6461 },
        startDate: "2024-03-01",
        endDate: "2024-08-31",
        predictedDelayRisk: "High"
    },
    {
        id: 4,
        projectName: "Park Development",
        description: "Development of Cubbon Park extension",
        wardNumber: "Ward 1",
        department: "BDA",
        status: "In Progress",
        budget: "₹30,00,000",
        location: { lat: 12.9762, lng: 77.6033 },
        startDate: "2024-02-01",
        endDate: "2024-07-31",
        predictedDelayRisk: "Low"
    },
    {
        id: 5,
        projectName: "Street Lighting Upgrade",
        description: "LED street lighting for Koramangala",
        wardNumber: "Ward 4",
        department: "BBMP",
        status: "Completed",
        budget: "₹15,00,000",
        location: { lat: 12.9352, lng: 77.6245 },
        startDate: "2023-10-01",
        endDate: "2024-01-31",
        predictedDelayRisk: "Low"
    }
];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize projects
    projects = [...sampleProjects];
    filteredProjects = [...projects];
    
    // Initialize map
    initializeMap();
    
    // Load projects
    loadProjects();
    
    // Check for existing user session
    checkExistingUser();
    
    // Setup event listeners
    setupEventListeners();
}

function checkExistingUser() {
    // Check localStorage for existing user
    const savedUser = localStorage.getItem('janata_audit_user');
    if (savedUser) {
        try {
            currentUser = JSON.parse(savedUser);
            updateLoginState();
            console.log('User session restored from localStorage');
        } catch (error) {
            console.error('Error parsing saved user data:', error);
            localStorage.removeItem('janata_audit_user');
        }
    }
}

function initializeMap() {
    // OpenStreetMap with Leaflet
    const bengaluru = [12.9716, 77.5946];
    map = L.map('map').setView(bengaluru, 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    addProjectMarkers();
}

function showMapError() {
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
        mapContainer.innerHTML = `
            <div style="
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                justify-content: center; 
                height: 100%; 
                background: #f8f9fa; 
                color: #6b7280;
                text-align: center;
                padding: 20px;
            ">
                <i class="fas fa-map-marked-alt" style="font-size: 48px; margin-bottom: 16px; color: #d1d5db;"></i>
                <h3 style="margin-bottom: 12px; color: #374151;">Google Maps Not Available</h3>
                <p style="margin-bottom: 16px; max-width: 400px;">
                    To enable the interactive map, you need to add a Google Maps API key.
                </p>
                <div style="background: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 16px; margin-bottom: 16px; max-width: 500px;">
                    <h4 style="color: #92400e; margin-bottom: 8px;">How to fix:</h4>
                    <ol style="text-align: left; color: #92400e; margin: 0; padding-left: 20px;">
                        <li>Get a Google Maps API key from <a href="https://console.cloud.google.com/" target="_blank" style="color: #92400e;">Google Cloud Console</a></li>
                        <li>Enable the Maps JavaScript API</li>
                        <li>Replace the commented script tag in index.html with your API key</li>
                    </ol>
                </div>
                <p style="font-size: 14px; color: #9ca3af;">
                    The application works without the map - you can still view all projects in the list below.
                </p>
            </div>
        `;
    }
}

function addProjectMarkers() {
    // Clear existing markers
    if (markers && markers.length) {
        markers.forEach(marker => map.removeLayer(marker));
    }
    markers = [];
    filteredProjects.forEach(project => {
        const marker = L.marker([project.location.lat, project.location.lng]).addTo(map);
        marker.bindPopup(createInfoWindowContent(project));
        markers.push(marker);
    });
}

function getMarkerColor(status) {
    switch (status) {
        case 'Completed':
            return '#28a745';
        case 'In Progress':
            return '#ffc107';
        case 'Pending':
            return '#dc3545';
        default:
            return '#6c757d';
    }
}

function createInfoWindowContent(project) {
    return `
        <div style="padding: 8px; max-width: 250px;">
            <h3 style="font-weight: bold; margin-bottom: 8px; color: #1f2937;">${project.projectName}</h3>
            <p style="font-size: 14px; color: #6b7280; margin-bottom: 8px;">${project.description}</p>
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span class="status-badge status-${project.status.toLowerCase().replace(' ', '-')}" style="
                    padding: 4px 8px; 
                    border-radius: 4px; 
                    font-size: 12px; 
                    font-weight: 500; 
                    text-transform: uppercase;
                    background: ${getMarkerColor(project.status)}20;
                    color: ${getMarkerColor(project.status)};
                ">${project.status}</span>
                ${project.predictedDelayRisk ? `
                    <span style="
                        font-size: 12px; 
                        font-weight: 500; 
                        padding: 4px 8px; 
                        border-radius: 4px;
                        background: ${getRiskColor(project.predictedDelayRisk)}20;
                        color: ${getRiskColor(project.predictedDelayRisk)};
                    ">Risk: ${project.predictedDelayRisk}</span>
                ` : ''}
            </div>
            <p style="font-size: 12px; color: #6b7280;">
                Ward: ${project.wardNumber} | ${project.department}
            </p>
            <p style="font-size: 12px; color: #6b7280;">
                Budget: ${project.budget}
            </p>
        </div>
    `;
}

function getRiskColor(risk) {
    switch (risk) {
        case 'High':
            return '#dc3545';
        case 'Medium':
            return '#ffc107';
        case 'Low':
            return '#28a745';
        default:
            return '#6c757d';
    }
}

function loadProjects() {
    updateProjectList();
    updateProjectCount();
}

function updateProjectList() {
    const projectListContent = document.getElementById('projectListContent');
    const projectsGrid = document.getElementById('projectsGrid');
    
    if (!projectListContent || !projectsGrid) return;
    
    // Update project list (sidebar)
    projectListContent.innerHTML = '';
    filteredProjects.slice(0, 10).forEach(project => {
        const projectCard = createProjectCard(project);
        projectListContent.appendChild(projectCard);
    });
    
    // Update projects grid (projects page)
    projectsGrid.innerHTML = '';
    filteredProjects.forEach(project => {
        const projectItem = createProjectItem(project);
        projectsGrid.appendChild(projectItem);
    });
}

function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    card.onclick = () => showProjectDetails(project);
    
    card.innerHTML = `
        <h4>${project.projectName}</h4>
        <p>${project.description}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
            <span class="project-status status-${project.status.toLowerCase().replace(' ', '-')}">${project.status}</span>
            <span style="font-size: 12px; color: #6b7280;">${project.wardNumber}</span>
        </div>
    `;
    
    return card;
}

function createProjectItem(project) {
    const item = document.createElement('div');
    item.className = 'project-item';
    item.onclick = () => showProjectDetails(project);
    
    item.innerHTML = `
        <h3>${project.projectName}</h3>
        <p>${project.description}</p>
        <div class="project-meta">
            <span class="project-status status-${project.status.toLowerCase().replace(' ', '-')}">${project.status}</span>
            <span style="font-size: 14px; color: #6b7280;">${project.budget}</span>
        </div>
    `;
    
    return item;
}

function updateProjectCount() {
    const projectCount = document.getElementById('projectCount');
    if (projectCount) {
        projectCount.textContent = filteredProjects.length;
    }
}

function applyFilters() {
    const wardFilter = document.getElementById('wardFilter').value;
    const departmentFilter = document.getElementById('departmentFilter').value;
    const statusFilter = document.getElementById('statusFilter').value;
    
    filteredProjects = projects.filter(project => {
        const wardMatch = !wardFilter || project.wardNumber === wardFilter;
        const departmentMatch = !departmentFilter || project.department === departmentFilter;
        const statusMatch = !statusFilter || project.status === statusFilter;
        
        return wardMatch && departmentMatch && statusMatch;
    });
    
    // Update map markers
    addProjectMarkers();
    
    // Update project list
    loadProjects();
}

function toggleFilterPanel() {
    const filterPanel = document.getElementById('filterPanel');
    if (filterPanel) {
        filterPanel.classList.toggle('show');
    }
}

function showLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.classList.add('show');
    }
}

function hideLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.classList.remove('show');
    }
}

function showProjectDetails(project) {
    const modal = document.getElementById('projectModal');
    const title = document.getElementById('projectModalTitle');
    const body = document.getElementById('projectModalBody');
    
    if (modal && title && body) {
        title.textContent = project.projectName;
        body.innerHTML = `
            <div style="margin-bottom: 20px;">
                <h3 style="color: #1f2937; margin-bottom: 12px;">Project Description</h3>
                <p style="color: #6b7280; line-height: 1.6;">${project.description}</p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px;">
                <div>
                    <h4 style="color: #374151; margin-bottom: 8px;">Ward Number</h4>
                    <p style="color: #6b7280;">${project.wardNumber}</p>
                </div>
                <div>
                    <h4 style="color: #374151; margin-bottom: 8px;">Department</h4>
                    <p style="color: #6b7280;">${project.department}</p>
                </div>
                <div>
                    <h4 style="color: #374151; margin-bottom: 8px;">Status</h4>
                    <span class="project-status status-${project.status.toLowerCase().replace(' ', '-')}">${project.status}</span>
                </div>
                <div>
                    <h4 style="color: #374151; margin-bottom: 8px;">Budget</h4>
                    <p style="color: #6b7280;">${project.budget}</p>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px;">
                <div>
                    <h4 style="color: #374151; margin-bottom: 8px;">Start Date</h4>
                    <p style="color: #6b7280;">${project.startDate}</p>
                </div>
                <div>
                    <h4 style="color: #374151; margin-bottom: 8px;">End Date</h4>
                    <p style="color: #6b7280;">${project.endDate}</p>
                </div>
                <div>
                    <h4 style="color: #374151; margin-bottom: 8px;">Delay Risk</h4>
                    <span style="
                        padding: 4px 8px; 
                        border-radius: 4px; 
                        font-size: 12px; 
                        font-weight: 500;
                        background: ${getRiskColor(project.predictedDelayRisk)}20;
                        color: ${getRiskColor(project.predictedDelayRisk)};
                    ">${project.predictedDelayRisk}</span>
                </div>
            </div>
            
            <div style="margin-top: 24px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                <h4 style="color: #374151; margin-bottom: 12px;">Actions</h4>
                <div style="display: flex; gap: 12px;">
                    <button onclick="viewOnMap('${project.id}')" style="
                        background: #2563eb; 
                        color: white; 
                        border: none; 
                        padding: 8px 16px; 
                        border-radius: 6px; 
                        cursor: pointer;
                        font-size: 14px;
                    ">View on Map</button>
                    <button onclick="submitFeedback('${project.id}')" style="
                        background: #10b981; 
                        color: white; 
                        border: none; 
                        padding: 8px 16px; 
                        border-radius: 6px; 
                        cursor: pointer;
                        font-size: 14px;
                    ">Submit Feedback</button>
                </div>
            </div>
        `;
        
        modal.classList.add('show');
    }
}

function hideProjectModal() {
    const modal = document.getElementById('projectModal');
    if (modal) {
        modal.classList.remove('show');
    }
}

function viewOnMap(projectId) {
    const project = projects.find(p => p.id == projectId);
    if (project && map) {
        map.setView([project.location.lat, project.location.lng], 15);
        hideProjectModal();
    }
}

function submitFeedback(projectId) {
    alert(`Feedback form for project ${projectId} would open here. This feature requires backend integration.`);
}

async function handleLogin(event) {
    event.preventDefault();
    
    const phoneNumber = document.getElementById('phoneNumber').value;
    const pincode = document.getElementById('pincode').value;
    const ward = document.getElementById('ward').value;
    
    showLoading();
    
    try {
        // Check if Firebase is available
        if (!auth) {
            throw new Error('Firebase not initialized. Using fallback authentication.');
        }
        
        // For now, we'll use a simple approach since phone auth requires additional setup
        // In a real app, you would use Firebase Phone Authentication
        
        // Create a user document in Firestore
        const userData = {
            phoneNumber: phoneNumber,
            pincode: pincode,
            ward: ward,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            lastLogin: firebase.firestore.FieldValue.serverTimestamp()
        };
        
        // Store user data in Firestore
        await db.collection('users').add(userData);
        
        // Set current user
        currentUser = {
            phoneNumber: phoneNumber,
            pincode: pincode,
            ward: ward,
            id: 'temp_user_id' // In real app, this would be the Firebase Auth UID
        };
        
        hideLoading();
        hideLoginModal();
        updateLoginState();
        
        alert('Login successful! Your data has been saved to Firebase.');
        
    } catch (error) {
        console.error('Login error:', error);
        hideLoading();
        
        // Fallback to local storage if Firebase fails
        const userData = {
            phoneNumber: phoneNumber,
            pincode: pincode,
            ward: ward,
            timestamp: new Date().toISOString()
        };
        
        // Store in localStorage as fallback
        localStorage.setItem('janata_audit_user', JSON.stringify(userData));
        
        currentUser = userData;
        hideLoginModal();
        updateLoginState();
        
        alert('Login successful! (Data saved locally - Firebase connection failed)');
    }
}

function updateLoginState() {
    const loginBtn = document.querySelector('.login-btn');
    if (loginBtn && currentUser) {
        loginBtn.innerHTML = `<i class="fas fa-user"></i> ${currentUser.phoneNumber}`;
        loginBtn.onclick = () => {
            if (confirm('Do you want to sign out?')) {
                currentUser = null;
                loginBtn.innerHTML = 'Sign In';
                loginBtn.onclick = showLoginModal;
            }
        };
    }
}

function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('href').substring(1);
            showSection(target);
            
            // Update active nav link
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
    
    // Close modals when clicking outside
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
            }
        });
    });
}

function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }
}

function showLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.add('show');
    }
}

function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.remove('show');
    }
}

function toggleMobileMenu() {
    // Mobile menu functionality would go here
    alert('Mobile menu functionality would be implemented here.');
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// API simulation functions (would connect to real backend)
async function fetchProjects() {
    // Simulate API call
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(sampleProjects);
        }, 1000);
    });
}

async function submitProjectFeedback(projectId, feedback) {
    // Simulate API call
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({ success: true, message: 'Feedback submitted successfully' });
        }, 1000);
    });
}

// Initialize when page loads
window.addEventListener('load', () => {
    console.log('Janata Audit Bengaluru - HTML Version Loaded');
});
