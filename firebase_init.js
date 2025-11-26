// Firebase Data Setup Script for Jannat Audit
// This script sets up initial Firestore collections and sample data

async function setupFirestoreCollections() {
    console.log('🏗️ Setting up Firestore collections for Jannat Audit...');
    
    try {
        // 1. System Configuration Collection
        await db.collection('system_config').doc('app_settings').set({
            app_name: 'Jannat Audit',
            version: '1.0.0',
            initialized_at: new Date(),
            data_sources: {
                eci: { enabled: true, last_updated: null },
                adr: { enabled: true, last_updated: null },
                mca: { enabled: true, last_updated: null }
            },
            features: {
                political_funding: true,
                bengaluru_projects: true,
                social_platform: true,
                ai_analysis: true
            }
        });
        
        // 2. Data Sources Status Collection
        await db.collection('data_sources').doc('eci').set({
            name: 'Election Commission of India',
            status: 'active',
            last_updated: new Date(),
            record_count: 247,
            data_type: 'political_funding'
        });
        
        await db.collection('data_sources').doc('adr').set({
            name: 'Association for Democratic Reforms',
            status: 'active',
            last_updated: new Date(),
            record_count: 189,
            data_type: 'political_analysis'
        });
        
        await db.collection('data_sources').doc('mca').set({
            name: 'Ministry of Corporate Affairs',
            status: 'active',
            last_updated: new Date(),
            record_count: 16,
            data_type: 'audit_reports'
        });
        
        // 3. Analytics Collection
        await db.collection('analytics').doc('platform_stats').set({
            total_funding_records: 247,
            total_audit_reports: 16,
            total_users: 0,
            total_interactions: 0,
            last_updated: new Date()
        });
        
        // 4. Sample Political Funding Data
        const sampleFundingData = [
            {
                id: 'sample_001',
                donor_name: 'Tech Solutions Pvt Ltd',
                recipient_party: 'Bharatiya Janata Party',
                amount: 25000000,
                date_of_purchase: '2024-03-15',
                data_type: 'electoral_bond',
                is_karnataka_party: true,
                is_karnataka_donor: true,
                donor_sector: 'Information Technology',
                donor_revenue: '500000000',
                donor_employees: 250,
                created_at: new Date()
            },
            {
                id: 'sample_002',
                donor_name: 'Karnataka Infrastructure Corp',
                recipient_party: 'Indian National Congress',
                amount: 15000000,
                date_of_purchase: '2024-02-20',
                data_type: 'electoral_bond',
                is_karnataka_party: true,
                is_karnataka_donor: true,
                donor_sector: 'Infrastructure',
                donor_revenue: '750000000',
                donor_employees: 180,
                created_at: new Date()
            }
        ];
        
        // Add sample funding data
        for (const donation of sampleFundingData) {
            await db.collection('political_funding').doc(donation.id).set(donation);
        }
        
        // 5. Sample Audit Reports
        const sampleAuditReports = [
            {
                id: 'audit_001',
                donor_name: 'Suspicious Donors Pvt Ltd',
                anomaly_type: 'Shell Company Risk',
                risk_score: 85,
                description: 'Company with minimal operations making large political donations',
                findings: [
                    'Low employee count relative to donation amount',
                    'Registered address is virtual office',
                    'Minimal business operations detected'
                ],
                created_at: new Date()
            },
            {
                id: 'audit_002',
                donor_name: 'Quick Money Ltd',
                anomaly_type: 'Timing Anomaly',
                risk_score: 72,
                description: 'Donation made immediately before major policy announcement',
                findings: [
                    'Donation timing correlates with policy decisions',
                    'No prior political donation history',
                    'Benefited from subsequent government contracts'
                ],
                created_at: new Date()
            }
        ];
        
        // Add sample audit reports
        for (const report of sampleAuditReports) {
            await db.collection('audit_reports').doc(report.id).set(report);
        }
        
        // 6. Connection Test Document
        await db.collection('system_config').doc('connection_test').set({
            status: 'active',
            message: 'Firebase connection is working properly',
            tested_at: new Date()
        });
        
        console.log('✅ Firestore collections setup complete!');
        console.log('📊 Created collections: system_config, data_sources, analytics, political_funding, audit_reports');
        
        return true;
        
    } catch (error) {
        console.warn('⚠️ Error setting up Firestore collections (insufficient permissions):', error.message);
        console.log('📱 App will continue in local-only mode with sample data');
        
        // Show user-friendly banner about Firebase status
        setTimeout(() => {
            if (typeof showFirebaseStatusBanner === 'function') {
                showFirebaseStatusBanner();
            }
        }, 2000); // Delay to ensure DOM is ready
        
        // Don't throw error - let app continue
        return false;
    }
}

// Function to verify collections are set up correctly
async function verifyFirestoreSetup() {
    try {
        console.log('🔍 Verifying Firestore setup...');
        
        // Check each collection
        const collections = ['system_config', 'data_sources', 'analytics', 'political_funding', 'audit_reports'];
        
        for (const collectionName of collections) {
            const snapshot = await db.collection(collectionName).limit(1).get();
            console.log(`✅ ${collectionName}: ${snapshot.size} documents found`);
        }
        
        console.log('✅ Firestore setup verification complete!');
        return true;
        
    } catch (error) {
        console.error('❌ Error verifying Firestore setup:', error);
        return false;
    }
}

// Auto-setup function (call this after Firebase is initialized)
async function autoSetupFirestore() {
    try {
        // Check if already setup
        const testDoc = await db.collection('system_config').doc('app_settings').get();
        
        if (!testDoc.exists) {
            console.log('🚀 First time setup detected. Setting up Firestore collections...');
            try {
                const setupResult = await setupFirestoreCollections();
                if (setupResult) {
                    console.log('✅ Firestore collections setup completed');
                } else {
                    console.log('📱 Running in local-only mode due to Firebase permissions');
                }
            } catch (setupError) {
                console.warn('⚠️ Firestore setup failed, but app will continue with local data:', setupError.message);
                // App continues to work with local/sample data
            }
        } else {
            console.log('✅ Firestore already configured');
        }
        
        // Try to verify setup, but don't fail if it doesn't work
        try {
            await verifyFirestoreSetup();
        } catch (verifyError) {
            console.warn('⚠️ Firestore verification failed, using local data mode:', verifyError.message);
        }
        
    } catch (error) {
        console.log('📱 Firebase auto-setup failed due to permissions, continuing in local mode');
        console.log('💡 This is normal - the app will work with sample data for demonstration');
        // Ensure the app continues to work even if Firebase fails completely
        initializeLocalDataMode();
    }
}

// Initialize local data mode when Firebase is unavailable
function initializeLocalDataMode() {
    console.log('🔧 Initializing local data mode...');
    
    // Set a flag to indicate we're in local mode
    if (typeof window !== 'undefined') {
        window.FIREBASE_AVAILABLE = false;
        window.LOCAL_DATA_MODE = true;
        
        // Trigger initialization of funding audit with local data
        if (typeof initializeFundingAudit === 'function') {
            setTimeout(() => {
                console.log('🚀 Starting funding audit in local mode...');
                initializeFundingAudit();
            }, 1000);
        }
    }
}

// Export functions for manual use
if (typeof window !== 'undefined') {
    window.setupFirestoreCollections = setupFirestoreCollections;
    window.verifyFirestoreSetup = verifyFirestoreSetup;
    window.autoSetupFirestore = autoSetupFirestore;
}