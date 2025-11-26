/**
 * Firebase Error Handler for Janata Audit
 * Handles network connectivity issues, blocked requests, and provides fallback mechanisms
 */

class FirebaseErrorHandler {
    constructor() {
        this.isOnline = navigator.onLine;
        this.connectionAttempts = 0;
        this.maxRetries = 3;
        this.retryDelay = 2000;
        this.fallbackMode = false;
        this.localDataCache = new Map();

        // Listen for online/offline events
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.handleConnectionRestored();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.handleConnectionLost();
        });

        // Set up error monitoring
        this.setupErrorMonitoring();
    }

    /**
     * Setup global error monitoring for Firebase-related errors
     */
    setupErrorMonitoring() {
        // Monitor console errors
        const originalError = console.error;
        console.error = (...args) => {
            this.handleConsoleError(args);
            originalError.apply(console, args);
        };

        // Monitor network errors
        window.addEventListener('error', (event) => {
            if (event.target && event.target.src &&
                (event.target.src.includes('firebase') ||
                    event.target.src.includes('firestore') ||
                    event.target.src.includes('googleapis'))) {
                this.handleNetworkError(event);
            }
        });

        // Monitor fetch errors
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            try {
                const response = await originalFetch.apply(window, args);
                return response;
            } catch (error) {
                if (args[0] && args[0].includes('googleapis')) {
                    this.handleFirebaseNetworkError(error, args[0]);
                }
                throw error;
            }
        };
    }

    /**
            (errorMessage.includes('firebase') && errorMessage.includes('network'))) {

            console.warn('🚫 Firebase connection blocked - switching to fallback mode');
            this.enableFallbackMode();
        }
    }

    /**
     * Handle network errors (blocked resources, etc.)
     */
    handleNetworkError(event) {
        console.warn('🌐 Network error detected:', event.target.src);

        if (event.target.src.includes('firestore') ||
            event.target.src.includes('googleapis')) {
            this.enableFallbackMode();
            this.showUserNotification('Connection blocked by ad blocker or network restrictions. Using offline mode.');
        }
    }

    /**
     * Handle Firebase-specific network errors
     */
    handleFirebaseNetworkError(error, url) {
        console.warn('🔥 Firebase network error:', error.message, url);

        if (error.message.includes('ERR_BLOCKED_BY_CLIENT') ||
            error.message.includes('Failed to fetch') ||
            error.message.includes('Network Error')) {
            this.enableFallbackMode();
        }
    }

    /**
     * Enable fallback mode when Firebase is unavailable
     */
    enableFallbackMode() {
        if (this.fallbackMode) return; // Already in fallback mode

        // If user is authenticated, we are likely NOT offline, so ignore false positives
        if (typeof firebase !== 'undefined' && firebase.auth && firebase.auth().currentUser) {
            console.log('🛡️ User is authenticated, ignoring fallback mode trigger');
            return;
        }

        this.fallbackMode = true;
        console.warn('📴 Enabling fallback mode - Firebase unavailable');

        // Update UI to show offline status
        this.updateUIForFallbackMode();

        // Load local data
        this.loadLocalData();

        // Disable Firebase-dependent features
        this.disableFirebaseFeatures();
    }

    /**
     * Disable Firebase-dependent features
     */
    disableFirebaseFeatures() {
        // Disable authentication features
        const authButtons = document.querySelectorAll('[data-requires-auth]');
        authButtons.forEach(btn => {
            btn.style.display = 'none';
        });

        // Disable real-time features
        const realtimeElements = document.querySelectorAll('[data-requires-realtime]');
        realtimeElements.forEach(element => {
            element.style.opacity = '0.5';
            element.title = 'Feature unavailable in offline mode';
        });

        // Show offline banner
        this.showOfflineBanner();
    }

    /**
     * Load local data when Firebase is unavailable
     */
    async loadLocalData() {
        try {
            // Load projects data from local JSON files
            const projectsResponse = await fetch('./bengaluru_projects.json');
            if (projectsResponse.ok) {
                const projectsData = await projectsResponse.json();
                this.localDataCache.set('projects', projectsData);
                console.log('📁 Loaded local projects data');
            }

            // Load government data
            const govResponse = await fetch('./government_data.json');
            if (govResponse.ok) {
                const govData = await govResponse.json();
                this.localDataCache.set('government_data', govData);
                console.log('📁 Loaded local government data');
            }

            // Load funding data
            const fundingResponse = await fetch('./political_funding_data.json');
            if (fundingResponse.ok) {
                const fundingData = await fundingResponse.json();
                this.localDataCache.set('funding_data', fundingData);
                console.log('📁 Loaded local funding data');
            }

            // Trigger data refresh in the main app
            if (window.refreshDataFromLocal) {
                window.refreshDataFromLocal(this.localDataCache);
            }

        } catch (error) {
            console.error('❌ Failed to load local data:', error);
        }
    }

    /**
     * Update UI to reflect fallback mode
     */
    updateUIForFallbackMode() {
        // Update connection status indicator
        const statusElement = document.getElementById('connection-status');
        if (statusElement) {
            statusElement.className = 'offline';
            statusElement.textContent = 'Offline Mode';
            statusElement.title = 'Firebase connection blocked or unavailable';
        }

        // Update Firebase status in UI
        if (window.updateFirebaseStatus) {
            window.updateFirebaseStatus('blocked');
        }
    }

    /**
     * Show offline banner to user
     */
    showOfflineBanner() {
        // Remove existing banner
        const existingBanner = document.getElementById('offline-banner');
        if (existingBanner) existingBanner.remove();

        // Create offline banner
        const banner = document.createElement('div');
        banner.id = 'offline-banner';
        banner.className = 'offline-banner';
        banner.innerHTML = `
            <div class="banner-content">
                <div class="banner-icon">📡</div>
                <div class="banner-text">
                    <strong>Offline Mode Active</strong>
                    <span>Firebase connection blocked. Using local data only.</span>
                </div>
                <div class="banner-actions">
                    <button onclick="firebaseErrorHandler.showConnectionHelp()" class="help-btn">Help</button>
                    <button onclick="firebaseErrorHandler.dismissBanner()" class="dismiss-btn">×</button>
                </div>
            </div>
        `;

        // Add banner styles
        const style = document.createElement('style');
        style.textContent = `
            .offline-banner {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #ff9500, #ff6b35);
                color: white;
                padding: 12px 20px;
                z-index: 10000;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                animation: slideDown 0.3s ease-out;
            }
            
            .banner-content {
                display: flex;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
                gap: 16px;
            }
            
            .banner-icon {
                font-size: 24px;
            }
            
            .banner-text {
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 4px;
            }
            
            .banner-text strong {
                font-weight: 600;
            }
            
            .banner-text span {
                font-size: 14px;
                opacity: 0.9;
            }
            
            .banner-actions {
                display: flex;
                gap: 8px;
            }
            
            .help-btn, .dismiss-btn {
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                transition: background 0.2s;
            }
            
            .help-btn:hover, .dismiss-btn:hover {
                background: rgba(255,255,255,0.3);
            }
            
            .dismiss-btn {
                padding: 6px 10px;
                font-size: 18px;
                line-height: 1;
            }
            
            @keyframes slideDown {
                from { transform: translateY(-100%); }
                to { transform: translateY(0); }
            }
        `;

        document.head.appendChild(style);
        document.body.insertBefore(banner, document.body.firstChild);
    }

    /**
     * Show connection help dialog
     */
    showConnectionHelp() {
        const helpModal = document.createElement('div');
        helpModal.className = 'connection-help-modal';
        helpModal.innerHTML = `
            <div class="modal-backdrop" onclick="this.parentElement.remove()"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h3>🔧 Connection Issues Help</h3>
                    <button onclick="this.closest('.connection-help-modal').remove()">×</button>
                </div>
                <div class="modal-body">
                    <div class="help-section">
                        <h4>Why is Firebase blocked?</h4>
                        <ul>
                            <li><strong>Ad Blockers:</strong> Extensions like uBlock Origin, AdBlock Plus may block Firebase/Google services</li>
                            <li><strong>Network Restrictions:</strong> Corporate firewalls or content filters</li>
                            <li><strong>Privacy Extensions:</strong> Privacy-focused browsers or extensions</li>
                            <li><strong>DNS Blocking:</strong> Pi-hole or similar network-level blocking</li>
                        </ul>
                    </div>
                    
                    <div class="help-section">
                        <h4>How to fix:</h4>
                        <ol>
                            <li><strong>Disable ad blocker</strong> for this site temporarily</li>
                            <li><strong>Whitelist domains:</strong> Add *.googleapis.com and *.firebase.com to allowlist</li>
                            <li><strong>Check browser extensions</strong> that might block tracking/analytics</li>
                            <li><strong>Try incognito mode</strong> to test without extensions</li>
                            <li><strong>Contact network admin</strong> if on corporate network</li>
                        </ol>
                    </div>
                    
                    <div class="help-section">
                        <h4>Current Status:</h4>
                        <div class="status-info">
                            <div>🌐 Internet: <span class="status ${this.isOnline ? 'online' : 'offline'}">${this.isOnline ? 'Connected' : 'Offline'}</span></div>
                            <div>🔥 Firebase: <span class="status offline">Blocked/Unavailable</span></div>
                            <div>📁 Local Data: <span class="status online">Available</span></div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button onclick="firebaseErrorHandler.retryConnection()" class="retry-btn">🔄 Retry Connection</button>
                    <button onclick="this.closest('.connection-help-modal').remove()" class="close-btn">Continue Offline</button>
                </div>
            </div>
        `;

        // Add modal styles
        const modalStyle = document.createElement('style');
        modalStyle.textContent = `
            .connection-help-modal {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: 10001;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .modal-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
            }
            
            .modal-content {
                background: white;
                border-radius: 12px;
                max-width: 600px;
                width: 100%;
                max-height: 80vh;
                overflow-y: auto;
                position: relative;
                box-shadow: 0 20px 40px rgba(0,0,0,0.15);
            }
            
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 24px 24px 16px;
                border-bottom: 1px solid #e5e5e5;
            }
            
            .modal-header h3 {
                margin: 0;
                color: #1a1a1a;
                font-size: 20px;
            }
            
            .modal-header button {
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                color: #666;
                padding: 0;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 6px;
            }
            
            .modal-header button:hover {
                background: #f5f5f5;
            }
            
            .modal-body {
                padding: 24px;
            }
            
            .help-section {
                margin-bottom: 24px;
            }
            
            .help-section h4 {
                color: #1a1a1a;
                margin: 0 0 12px 0;
                font-size: 16px;
            }
            
            .help-section ul, .help-section ol {
                margin: 0;
                padding-left: 20px;
            }
            
            .help-section li {
                margin-bottom: 8px;
                line-height: 1.5;
            }
            
            .status-info {
                background: #f8f9fa;
                padding: 16px;
                border-radius: 8px;
                font-family: monospace;
            }
            
            .status-info div {
                margin-bottom: 8px;
                display: flex;
                justify-content: space-between;
            }
            
            .status-info div:last-child {
                margin-bottom: 0;
            }
            
            .status.online {
                color: #28a745;
                font-weight: 600;
            }
            
            .status.offline {
                color: #dc3545;
                font-weight: 600;
            }
            
            .modal-footer {
                padding: 16px 24px 24px;
                display: flex;
                gap: 12px;
                justify-content: flex-end;
            }
            
            .retry-btn, .close-btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 500;
                transition: all 0.2s;
            }
            
            .retry-btn {
                background: #3c8ce7;
                color: white;
            }
            
            .retry-btn:hover {
                background: #2b7cd6;
            }
            
            .close-btn {
                background: #f8f9fa;
                color: #6c757d;
                border: 1px solid #dee2e6;
            }
            
            .close-btn:hover {
                background: #e9ecef;
            }
        `;

        document.head.appendChild(modalStyle);
        document.body.appendChild(helpModal);
    }

    /**
     * Dismiss the offline banner
     */
    dismissBanner() {
        const banner = document.getElementById('offline-banner');
        if (banner) {
            banner.style.animation = 'slideUp 0.3s ease-out forwards';
            setTimeout(() => banner.remove(), 300);
        }

        // Add slideUp animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideUp {
                from { transform: translateY(0); }
                to { transform: translateY(-100%); }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Retry Firebase connection
     */
    async retryConnection() {
        if (this.connectionAttempts >= this.maxRetries) {
            console.warn('⚠️ Max connection retries reached');
            this.showUserNotification('Maximum retry attempts reached. Please check your connection settings.');
            return;
        }

        this.connectionAttempts++;
        console.log(`🔄 Retrying Firebase connection (attempt ${this.connectionAttempts}/${this.maxRetries})`);

        // Show loading state
        this.showUserNotification('Retrying connection...', 'info');

        try {
            // Wait before retry
            await new Promise(resolve => setTimeout(resolve, this.retryDelay));

            // Try to reinitialize Firebase
            if (window.initializeFirebase) {
                await window.initializeFirebase();

                // Test connection
                if (window.testFirestoreConnection) {
                    await window.testFirestoreConnection();
                }

                // If successful, disable fallback mode
                this.disableFallbackMode();
                this.showUserNotification('Connection restored!', 'success');

            }
        } catch (error) {
            console.error('❌ Retry failed:', error);
            this.showUserNotification('Retry failed. Please check your connection settings.', 'error');
        }
    }

    /**
     * Disable fallback mode when connection is restored
     */
    disableFallbackMode() {
        this.fallbackMode = false;
        this.connectionAttempts = 0;

        // Remove offline banner
        this.dismissBanner();

        // Re-enable Firebase features
        const authButtons = document.querySelectorAll('[data-requires-auth]');
        authButtons.forEach(btn => {
            btn.style.display = '';
        });

        const realtimeElements = document.querySelectorAll('[data-requires-realtime]');
        realtimeElements.forEach(element => {
            element.style.opacity = '';
            element.title = '';
        });

        // Update UI status
        if (window.updateFirebaseStatus) {
            window.updateFirebaseStatus('connected');
        }

        console.log('✅ Fallback mode disabled - Firebase connection restored');
    }

    /**
     * Handle connection restored
     */
    handleConnectionRestored() {
        console.log('🌐 Internet connection restored');
        if (this.fallbackMode) {
            this.retryConnection();
        }
    }

    /**
     * Handle connection lost
     */
    handleConnectionLost() {
        console.log('📡 Internet connection lost');
        this.enableFallbackMode();
    }

    /**
     * Show user notification
     */
    showUserNotification(message, type = 'warning') {
        // Remove existing notifications
        const existing = document.querySelectorAll('.firebase-notification');
        existing.forEach(n => n.remove());

        const notification = document.createElement('div');
        notification.className = `firebase-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${this.getNotificationIcon(type)}</span>
                <span class="notification-message">${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="notification-close">×</button>
            </div>
        `;

        // Add notification styles
        const style = document.createElement('style');
        style.textContent = `
            .firebase-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                max-width: 400px;
                padding: 16px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 10000;
                animation: slideInRight 0.3s ease-out;
            }
            
            .firebase-notification.warning {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
            }
            
            .firebase-notification.error {
                background: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
            }
            
            .firebase-notification.success {
                background: #d1edff;
                border: 1px solid #bee5eb;
                color: #0c5460;
            }
            
            .firebase-notification.info {
                background: #d1ecf1;
                border: 1px solid #bee5eb;
                color: #0c5460;
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .notification-icon {
                font-size: 20px;
            }
            
            .notification-message {
                flex: 1;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .notification-close {
                background: none;
                border: none;
                font-size: 18px;
                cursor: pointer;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 4px;
                opacity: 0.7;
            }
            
            .notification-close:hover {
                opacity: 1;
                background: rgba(0,0,0,0.1);
            }
            
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(notification);

        // Auto-remove after 5 seconds for non-error messages
        if (type !== 'error') {
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.style.animation = 'slideOutRight 0.3s ease-out forwards';
                    setTimeout(() => notification.remove(), 300);
                }
            }, 5000);
        }
    }

    /**
     * Get notification icon based on type
     */
    getNotificationIcon(type) {
        const icons = {
            warning: '⚠️',
            error: '❌',
            success: '✅',
            info: 'ℹ️'
        };
        return icons[type] || '📢';
    }

    /**
     * Get cached local data
     */
    getLocalData(key) {
        return this.localDataCache.get(key);
    }

    /**
     * Check if in fallback mode
     */
    isFallbackMode() {
        return this.fallbackMode;
    }

    /**
     * Get connection status
     */
    getConnectionStatus() {
        return {
            online: this.isOnline,
            fallbackMode: this.fallbackMode,
            connectionAttempts: this.connectionAttempts
        };
    }
}

// Initialize error handler when script loads
let firebaseErrorHandler;

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        firebaseErrorHandler = new FirebaseErrorHandler();
        console.log('🛡️ Firebase Error Handler initialized');
    });
} else {
    firebaseErrorHandler = new FirebaseErrorHandler();
    console.log('🛡️ Firebase Error Handler initialized');
}

// Export for global access
if (typeof window !== 'undefined') {
    window.firebaseErrorHandler = firebaseErrorHandler;
}
