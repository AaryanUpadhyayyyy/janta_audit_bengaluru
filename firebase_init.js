// Firebase Initialization Script for Janata Audit Bengaluru
// This script sets up the database and ensures proper connection

class FirebaseInitializer {
    constructor() {
        this.isInitialized = false;
        this.db = null;
        this.auth = null;
    }

    // Initialize Firebase connection
    async initialize() {
        try {
            console.log('🔥 Initializing Firebase...');
            
            // Check if Firebase is available
            if (typeof window !== 'undefined' && window.firebaseDb && window.firebaseAuth) {
                this.db = window.firebaseDb;
                this.auth = window.firebaseAuth;
                this.isInitialized = true;
                console.log('✅ Firebase initialized successfully');
                return true;
            } else {
                console.log('⚠️ Firebase not available, using mock data');
                return false;
            }
        } catch (error) {
            console.error('❌ Firebase initialization failed:', error);
            return false;
        }
    }

    // Create database collections and sample data
    async setupDatabase() {
        if (!this.isInitialized) {
            console.log('⚠️ Firebase not initialized, skipping database setup');
            return;
        }

        try {
            console.log('🗄️ Setting up database collections...');
            
            // Import Firestore functions
            const { collection, addDoc, getDocs, query, where } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
            
            // Check if collections exist and create sample data
            await this.createSampleUsers();
            await this.createSampleProjects();
            await this.createSampleFeedback();
            
            console.log('✅ Database setup complete');
        } catch (error) {
            console.error('❌ Database setup failed:', error);
        }
    }

    // Create sample users
    async createSampleUsers() {
        try {
            const { collection, addDoc, getDocs, query, where } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
            
            // Check if users collection has data
            const usersQuery = query(collection(this.db, 'users'));
            const usersSnapshot = await getDocs(usersQuery);
            
            if (usersSnapshot.empty) {
                console.log('👥 Creating sample users...');
                
                const sampleUsers = [
                    {
                        uid: 'demo-admin-123',
                        email: 'admin@janataaudit.com',
                        name: 'Admin User',
                        role: 'admin',
                        createdAt: new Date(),
                        updatedAt: new Date()
                    },
                    {
                        uid: 'demo-citizen-456',
                        email: 'citizen@example.com',
                        name: 'John Citizen',
                        role: 'citizen',
                        createdAt: new Date(),
                        updatedAt: new Date()
                    }
                ];

                for (const user of sampleUsers) {
                    await addDoc(collection(this.db, 'users'), user);
                    console.log(`✅ Created user: ${user.name}`);
                }
            } else {
                console.log('👥 Users collection already has data');
            }
        } catch (error) {
            console.error('❌ Error creating sample users:', error);
        }
    }

    // Create sample projects
    async createSampleProjects() {
        try {
            const { collection, addDoc, getDocs, query, where } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
            
            // Check if projects collection has data
            const projectsQuery = query(collection(this.db, 'projects'));
            const projectsSnapshot = await getDocs(projectsQuery);
            
            if (projectsSnapshot.empty) {
                console.log('🏗️ Creating sample projects...');
                
                const sampleProjects = [
                    {
                        projectName: "BBMP Smart City Initiative",
                        description: "Implementation of smart city technologies across Bengaluru",
                        budget: 50000000,
                        status: "In Progress",
                        department: "BBMP",
                        location: "Bengaluru",
                        wardNumber: "Ward 1",
                        startDate: new Date('2024-01-01'),
                        endDate: new Date('2024-12-31'),
                        geoPoint: { latitude: 12.9716, longitude: 77.5946 },
                        createdAt: new Date(),
                        updatedAt: new Date()
                    },
                    {
                        projectName: "BMRCL Metro Phase 3",
                        description: "Extension of metro lines to outer areas of Bengaluru",
                        budget: 75000000,
                        status: "Pending",
                        department: "BMRCL",
                        location: "Whitefield, Bengaluru",
                        wardNumber: "Ward 5",
                        startDate: new Date('2024-06-01'),
                        endDate: new Date('2025-12-31'),
                        geoPoint: { latitude: 12.9698, longitude: 77.7500 },
                        createdAt: new Date(),
                        updatedAt: new Date()
                    },
                    {
                        projectName: "BWSSB Water Supply Network",
                        description: "Upgradation of water supply infrastructure",
                        budget: 30000000,
                        status: "Completed",
                        department: "BWSSB",
                        location: "Electronic City, Bengaluru",
                        wardNumber: "Ward 8",
                        startDate: new Date('2023-06-01'),
                        endDate: new Date('2024-05-31'),
                        geoPoint: { latitude: 12.8456, longitude: 77.6603 },
                        createdAt: new Date(),
                        updatedAt: new Date()
                    }
                ];

                for (const project of sampleProjects) {
                    await addDoc(collection(this.db, 'projects'), project);
                    console.log(`✅ Created project: ${project.projectName}`);
                }
            } else {
                console.log('🏗️ Projects collection already has data');
            }
        } catch (error) {
            console.error('❌ Error creating sample projects:', error);
        }
    }

    // Create sample feedback
    async createSampleFeedback() {
        try {
            const { collection, addDoc, getDocs, query, where } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
            
            // Check if feedback collection has data
            const feedbackQuery = query(collection(this.db, 'feedback'));
            const feedbackSnapshot = await getDocs(feedbackQuery);
            
            if (feedbackSnapshot.empty) {
                console.log('💬 Creating sample feedback...');
                
                const sampleFeedback = [
                    {
                        projectId: "project-1",
                        projectName: "BBMP Smart City Initiative",
                        user: "John Citizen",
                        email: "citizen@example.com",
                        category: "Infrastructure",
                        rating: 4,
                        comment: "Great initiative! The smart city project is progressing well.",
                        location: "Bengaluru",
                        status: "approved",
                        createdAt: new Date()
                    },
                    {
                        projectId: "project-2",
                        projectName: "BMRCL Metro Phase 3",
                        user: "Sarah Kumar",
                        email: "sarah@example.com",
                        category: "Transport",
                        rating: 5,
                        comment: "Excellent metro connectivity. This will greatly improve our daily commute.",
                        location: "Whitefield, Bengaluru",
                        status: "pending",
                        createdAt: new Date()
                    }
                ];

                for (const feedback of sampleFeedback) {
                    await addDoc(collection(this.db, 'feedback'), feedback);
                    console.log(`✅ Created feedback: ${feedback.comment.substring(0, 50)}...`);
                }
            } else {
                console.log('💬 Feedback collection already has data');
            }
        } catch (error) {
            console.error('❌ Error creating sample feedback:', error);
        }
    }

    // Test Firebase connection
    async testConnection() {
        if (!this.isInitialized) {
            console.log('⚠️ Firebase not initialized, cannot test connection');
            return false;
        }

        try {
            console.log('🔍 Testing Firebase connection...');
            
            const { collection, getDocs } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
            
            // Test reading from users collection
            const usersSnapshot = await getDocs(collection(this.db, 'users'));
            console.log(`✅ Users collection: ${usersSnapshot.size} documents`);
            
            // Test reading from projects collection
            const projectsSnapshot = await getDocs(collection(this.db, 'projects'));
            console.log(`✅ Projects collection: ${projectsSnapshot.size} documents`);
            
            // Test reading from feedback collection
            const feedbackSnapshot = await getDocs(collection(this.db, 'feedback'));
            console.log(`✅ Feedback collection: ${feedbackSnapshot.size} documents`);
            
            console.log('🎉 Firebase connection test successful!');
            return true;
        } catch (error) {
            console.error('❌ Firebase connection test failed:', error);
            return false;
        }
    }

    // Run complete initialization
    async run() {
        console.log('🚀 Starting Firebase initialization...');
        
        const initialized = await this.initialize();
        if (initialized) {
            await this.setupDatabase();
            await this.testConnection();
            console.log('✅ Firebase initialization complete!');
        } else {
            console.log('⚠️ Firebase initialization skipped, using mock data');
        }
    }
}

// Auto-initialize when page loads
document.addEventListener('DOMContentLoaded', async () => {
    const firebaseInit = new FirebaseInitializer();
    await firebaseInit.run();
});

// Make available globally
window.FirebaseInitializer = FirebaseInitializer;
