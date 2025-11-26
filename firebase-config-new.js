// Firebase Configuration for Janata Audit Bengaluru
// Replace the placeholders with your actual Firebase project configuration

const firebaseConfig = {
    // REQUIRED: You must add your API Key here
    apiKey: "AIzaSyDKHPTc0Sqnhlg_5IFfo7Ty-6USsFbMSCk",

    // Derived from your project ID: janta-audit-3c182
    authDomain: "janta-audit-3c182.firebaseapp.com",
    projectId: "janta-audit-3c182",
    storageBucket: "janta-audit-3c182.appspot.com",

    // Your Project Number
    messagingSenderId: "853121342619",

    // REQUIRED: You must add your App ID here
    appId: "1:853121342619:web:66e7a7cad03f622fdafa3e"
};

// Initialize Firebase
if (typeof firebase !== 'undefined') {
    try {
        firebase.initializeApp(firebaseConfig);
        console.log('🔥 Firebase initialized with config');
    } catch (error) {
        console.error('❌ Firebase initialization error:', error);
        // Check if it's a "already initialized" error
        if (error.code === 'app/duplicate-app') {
            console.log('⚠️ Firebase already initialized, ignoring');
        }
    }
} else {
    console.error('❌ Firebase SDK not loaded');
}
