// Authentication System for Janata Audit Bengaluru
class AuthSystem {
    constructor() {
        this.currentUser = null;
        this.isAuthenticated = false;
        this.init();
    }

    init() {
        // Check if user is already logged in
        const user = localStorage.getItem('user');
        if (user) {
            this.currentUser = JSON.parse(user);
            this.isAuthenticated = true;
        }
        // Always update UI to show appropriate buttons
        this.updateUI();
    }

    // Sign in function
    async signIn(email, password) {
        try {
            // Try Firebase authentication first
            if (window.firebaseAuth) {
                const { signInWithEmailAndPassword } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js');
                const userCredential = await signInWithEmailAndPassword(window.firebaseAuth, email, password);
                
                // Get user profile from Firestore
                const { collection, query, where, getDocs } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
                const usersQuery = query(collection(window.firebaseDb, 'users'), where('uid', '==', userCredential.user.uid));
                const usersSnapshot = await getDocs(usersQuery);
                
                let userProfile = {
                    uid: userCredential.user.uid,
                    email: userCredential.user.email,
                    name: userCredential.user.displayName || 'User',
                    role: 'citizen'
                };
                
                if (!usersSnapshot.empty) {
                    const userDoc = usersSnapshot.docs[0].data();
                    userProfile = { ...userProfile, ...userDoc };
                }
                
                this.currentUser = userProfile;
                this.isAuthenticated = true;
                localStorage.setItem('user', JSON.stringify(this.currentUser));
                this.updateUI();
                return { success: true, user: this.currentUser };
            }
        } catch (firebaseError) {
            console.log('Firebase auth failed, trying mock auth:', firebaseError.message);
        }

        try {
            // Fallback to API call
            const response = await fetch('/api/auth/signin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                this.currentUser = data.user;
                this.isAuthenticated = true;
                localStorage.setItem('user', JSON.stringify(this.currentUser));
                this.updateUI();
                return { success: true, user: this.currentUser };
            } else {
                const error = await response.json();
                return { success: false, error: error.message };
            }
        } catch (error) {
            // Final fallback to mock authentication for demo
            if (email === 'admin@janataaudit.com' && password === 'admin123') {
                this.currentUser = {
                    uid: 'demo-user-123',
                    email: email,
                    name: 'Admin User',
                    role: 'admin'
                };
                this.isAuthenticated = true;
                localStorage.setItem('user', JSON.stringify(this.currentUser));
                this.updateUI();
                return { success: true, user: this.currentUser };
            } else {
                return { success: false, error: 'Invalid credentials' };
            }
        }
    }

    // Sign up function
    async signUp(email, password, name) {
        try {
            // Try Firebase authentication first
            if (window.firebaseAuth && window.firebaseDb) {
                const { createUserWithEmailAndPassword } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js');
                const { collection, addDoc } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
                
                const userCredential = await createUserWithEmailAndPassword(window.firebaseAuth, email, password);
                
                // Add user profile to Firestore
                const userData = {
                    uid: userCredential.user.uid,
                    email: email,
                    name: name,
                    createdAt: new Date(),
                    updatedAt: new Date(),
                    role: 'citizen'
                };
                
                await addDoc(collection(window.firebaseDb, 'users'), userData);
                
                this.currentUser = {
                    uid: userCredential.user.uid,
                    email: email,
                    name: name,
                    role: 'citizen'
                };
                this.isAuthenticated = true;
                localStorage.setItem('user', JSON.stringify(this.currentUser));
                this.updateUI();
                return { success: true, user: this.currentUser };
            }
        } catch (firebaseError) {
            console.log('Firebase signup failed, trying mock auth:', firebaseError.message);
        }

        try {
            // Fallback to API call
            const response = await fetch('/api/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password, name })
            });

            if (response.ok) {
                const data = await response.json();
                this.currentUser = data.user;
                this.isAuthenticated = true;
                localStorage.setItem('user', JSON.stringify(this.currentUser));
                this.updateUI();
                return { success: true, user: this.currentUser };
            } else {
                const error = await response.json();
                return { success: false, error: error.message };
            }
        } catch (error) {
            // Final fallback to mock registration for demo
            this.currentUser = {
                uid: 'demo-user-' + Date.now(),
                email: email,
                name: name,
                role: 'citizen'
            };
            this.isAuthenticated = true;
            localStorage.setItem('user', JSON.stringify(this.currentUser));
            this.updateUI();
            return { success: true, user: this.currentUser };
        }
    }

    // Sign out function
    signOut() {
        this.currentUser = null;
        this.isAuthenticated = false;
        localStorage.removeItem('user');
        this.updateUI();
        window.location.href = '/';
    }

    // Update UI based on auth state
    updateUI() {
        const authButtons = document.getElementById('authButtons');
        const userMenu = document.getElementById('userMenu');
        const signInModal = document.getElementById('signInModal');
        const signUpModal = document.getElementById('signUpModal');

        if (this.isAuthenticated) {
            // Show user menu
            if (authButtons) authButtons.style.display = 'none';
            if (userMenu) {
                userMenu.style.display = 'block';
                userMenu.innerHTML = `
                    <div class="user-info">
                        <span class="user-name">${this.currentUser.name}</span>
                        <span class="user-role">${this.currentUser.role}</span>
                    </div>
                    <div class="user-actions">
                        <a href="logout.html" class="btn btn-secondary">Sign Out</a>
                    </div>
                `;
            }
        } else {
            // Show auth buttons
            if (authButtons) authButtons.style.display = 'block';
            if (userMenu) userMenu.style.display = 'none';
        }
    }

    // Show sign in modal
    showSignIn() {
        const modal = document.getElementById('signInModal');
        if (modal) modal.style.display = 'flex';
    }

    // Show sign up modal
    showSignUp() {
        const modal = document.getElementById('signUpModal');
        if (modal) modal.style.display = 'flex';
    }

    // Hide modals
    hideModals() {
        const modals = document.querySelectorAll('.auth-modal');
        modals.forEach(modal => modal.style.display = 'none');
    }

    // Handle sign in form
    async handleSignIn(event) {
        event.preventDefault();
        const form = event.target;
        const email = form.email.value;
        const password = form.password.value;

        const result = await this.signIn(email, password);
        
        if (result.success) {
            this.hideModals();
            showNotification('Successfully signed in!', 'success');
        } else {
            showNotification(result.error, 'error');
        }
    }

    // Handle sign up form
    async handleSignUp(event) {
        event.preventDefault();
        const form = event.target;
        const email = form.email.value;
        const password = form.password.value;
        const name = form.name.value;

        const result = await this.signUp(email, password, name);
        
        if (result.success) {
            this.hideModals();
            showNotification('Account created successfully!', 'success');
        } else {
            showNotification(result.error, 'error');
        }
    }
}

// Initialize auth system
const authSystem = new AuthSystem();

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="notification-close">×</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Export for global use
window.authSystem = authSystem;
window.showNotification = showNotification;
