// Database Migration Script for Janata Audit Bengaluru
// This script helps migrate existing data to Firebase

// Import Firebase functions
import { 
    getProjects, 
    addProject, 
    getFeedback, 
    submitFeedback,
    signInUser,
    signUpUser 
} from './firebase-config.js';

class DatabaseMigration {
    constructor() {
        this.migratedProjects = 0;
        this.migratedFeedback = 0;
        this.errors = [];
    }

    // Migrate projects from JSON to Firebase
    async migrateProjects() {
        console.log('🚀 Starting project migration...');
        
        try {
            // Get existing projects from API
            const response = await fetch('/api/projects');
            const data = await response.json();
            
            if (!data.projects || data.projects.length === 0) {
                console.log('❌ No projects found to migrate');
                return;
            }

            console.log(`📊 Found ${data.projects.length} projects to migrate`);

            // Migrate each project
            for (const project of data.projects) {
                try {
                    const result = await addProject(project);
                    if (result.success) {
                        this.migratedProjects++;
                        console.log(`✅ Migrated: ${project.projectName}`);
                    } else {
                        this.errors.push(`Failed to migrate ${project.projectName}: ${result.error}`);
                    }
                } catch (error) {
                    this.errors.push(`Error migrating ${project.projectName}: ${error.message}`);
                }
            }

            console.log(`🎉 Project migration complete! Migrated ${this.migratedProjects} projects`);
            
        } catch (error) {
            console.error('❌ Migration failed:', error);
            this.errors.push(`Migration failed: ${error.message}`);
        }
    }

    // Migrate feedback data
    async migrateFeedback() {
        console.log('🚀 Starting feedback migration...');
        
        try {
            // Get existing feedback from API
            const response = await fetch('/api/feedback');
            const data = await response.json();
            
            if (!data.feedback || data.feedback.length === 0) {
                console.log('❌ No feedback found to migrate');
                return;
            }

            console.log(`📊 Found ${data.feedback.length} feedback items to migrate`);

            // Migrate each feedback
            for (const feedback of data.feedback) {
                try {
                    const result = await submitFeedback(feedback);
                    if (result.success) {
                        this.migratedFeedback++;
                        console.log(`✅ Migrated feedback: ${feedback.comment.substring(0, 50)}...`);
                    } else {
                        this.errors.push(`Failed to migrate feedback: ${result.error}`);
                    }
                } catch (error) {
                    this.errors.push(`Error migrating feedback: ${error.message}`);
                }
            }

            console.log(`🎉 Feedback migration complete! Migrated ${this.migratedFeedback} feedback items`);
            
        } catch (error) {
            console.error('❌ Feedback migration failed:', error);
            this.errors.push(`Feedback migration failed: ${error.message}`);
        }
    }

    // Create sample data for testing
    async createSampleData() {
        console.log('🚀 Creating sample data...');
        
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
                geoPoint: { latitude: 12.9716, longitude: 77.5946 }
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
                geoPoint: { latitude: 12.9698, longitude: 77.7500 }
            }
        ];

        for (const project of sampleProjects) {
            try {
                const result = await addProject(project);
                if (result.success) {
                    console.log(`✅ Created sample project: ${project.projectName}`);
                }
            } catch (error) {
                console.error(`❌ Failed to create sample project: ${error.message}`);
            }
        }
    }

    // Test database connection
    async testConnection() {
        console.log('🔍 Testing database connection...');
        
        try {
            // Test projects collection
            const projectsResult = await getProjects();
            if (projectsResult.success) {
                console.log(`✅ Projects collection accessible: ${projectsResult.projects.length} projects`);
            } else {
                console.error('❌ Projects collection error:', projectsResult.error);
            }

            // Test feedback collection
            const feedbackResult = await getFeedback();
            if (feedbackResult.success) {
                console.log(`✅ Feedback collection accessible: ${feedbackResult.feedback.length} feedback items`);
            } else {
                console.error('❌ Feedback collection error:', feedbackResult.error);
            }

        } catch (error) {
            console.error('❌ Database connection test failed:', error);
        }
    }

    // Run complete migration
    async runMigration() {
        console.log('🚀 Starting complete database migration...');
        console.log('=====================================');
        
        // Test connection first
        await this.testConnection();
        
        // Migrate projects
        await this.migrateProjects();
        
        // Migrate feedback
        await this.migrateFeedback();
        
        // Create sample data if needed
        if (this.migratedProjects === 0) {
            await this.createSampleData();
        }
        
        // Print summary
        console.log('=====================================');
        console.log('📊 Migration Summary:');
        console.log(`✅ Projects migrated: ${this.migratedProjects}`);
        console.log(`✅ Feedback migrated: ${this.migratedFeedback}`);
        console.log(`❌ Errors: ${this.errors.length}`);
        
        if (this.errors.length > 0) {
            console.log('🚨 Errors encountered:');
            this.errors.forEach(error => console.log(`  - ${error}`));
        }
        
        console.log('🎉 Migration complete!');
    }

    // Clear all data (use with caution)
    async clearAllData() {
        console.log('⚠️ Clearing all data...');
        
        try {
            // This would require additional Firebase functions
            console.log('❌ Clear data function not implemented for safety');
            console.log('💡 Use Firebase Console to manually clear data if needed');
        } catch (error) {
            console.error('❌ Clear data failed:', error);
        }
    }
}

// Make migration available globally
window.DatabaseMigration = DatabaseMigration;

// Auto-run migration if Firebase is available
document.addEventListener('DOMContentLoaded', async () => {
    // Wait a bit for Firebase to initialize
    setTimeout(async () => {
        if (window.firebaseAuth && window.firebaseDb) {
            console.log('🔥 Firebase detected! Migration tools available.');
            console.log('💡 Run: new DatabaseMigration().runMigration() to start migration');
        } else {
            console.log('❌ Firebase not detected. Please set up Firebase first.');
        }
    }, 2000);
});

export default DatabaseMigration;
