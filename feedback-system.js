// Feedback System for Janata Audit Bengaluru
class FeedbackSystem {
    constructor() {
        this.feedback = [];
        this.init();
    }

    init() {
        this.loadFeedback();
    }

    // Load feedback from API
    async loadFeedback() {
        try {
            const response = await fetch('/api/feedback');
            if (response.ok) {
                const data = await response.json();
                this.feedback = data.feedback || [];
            }
        } catch (error) {
            console.log('Using mock feedback data');
            this.feedback = this.getMockFeedback();
        }
    }

    // Get mock feedback data
    getMockFeedback() {
        return [
            {
                id: '1',
                projectId: 'BBMP_MOCK_1',
                projectName: 'BBMP Ward 15 Road Development Project',
                user: 'Citizen User',
                rating: 4,
                comment: 'The road development is progressing well. Good quality work being done.',
                category: 'Infrastructure',
                status: 'approved',
                createdAt: new Date('2024-01-15'),
                location: 'Ward 15, Bengaluru'
            },
            {
                id: '2',
                projectId: 'BMRCL_MOCK_5',
                projectName: 'BMRCL Purple Line Extension Phase 2',
                user: 'Local Resident',
                rating: 5,
                comment: 'Excellent metro connectivity. This will greatly improve our daily commute.',
                category: 'Transport',
                status: 'pending',
                createdAt: new Date('2024-01-20'),
                location: 'Whitefield, Bengaluru'
            },
            {
                id: '3',
                projectId: 'BWSSB_MOCK_3',
                projectName: 'BWSSB Cauvery Water Supply Phase 5',
                user: 'Community Leader',
                rating: 3,
                comment: 'Water supply project is delayed. Need better coordination with local authorities.',
                category: 'Water Supply',
                status: 'under_review',
                createdAt: new Date('2024-01-25'),
                location: 'Electronic City, Bengaluru'
            }
        ];
    }

    // Submit feedback
    async submitFeedback(feedbackData) {
        try {
            // Try Firebase first
            if (window.firebaseDb) {
                const { collection, addDoc } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
                
                const feedbackToSave = {
                    ...feedbackData,
                    createdAt: new Date(),
                    updatedAt: new Date(),
                    status: 'pending'
                };
                
                const docRef = await addDoc(collection(window.firebaseDb, 'feedback'), feedbackToSave);
                
                const newFeedback = {
                    id: docRef.id,
                    ...feedbackToSave
                };
                
                this.feedback.unshift(newFeedback);
                this.displayFeedback();
                console.log('✅ Feedback saved to Firebase:', newFeedback);
                return { success: true, feedback: newFeedback };
            }
        } catch (firebaseError) {
            console.log('Firebase feedback submission failed, trying API:', firebaseError.message);
        }

        try {
            // Fallback to API call
            const response = await fetch('/api/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(feedbackData)
            });

            if (response.ok) {
                const data = await response.json();
                this.feedback.unshift(data.feedback);
                this.displayFeedback();
                return { success: true, feedback: data.feedback };
            } else {
                const error = await response.json();
                return { success: false, error: error.message };
            }
        } catch (error) {
            // Final fallback to mock submission
            const newFeedback = {
                id: Date.now().toString(),
                ...feedbackData,
                status: 'pending',
                createdAt: new Date()
            };
            this.feedback.unshift(newFeedback);
            this.displayFeedback();
            return { success: true, feedback: newFeedback };
        }
    }

    // Display feedback
    displayFeedback() {
        const feedbackContainer = document.getElementById('feedbackContainer');
        if (!feedbackContainer) return;

        if (this.feedback.length === 0) {
            feedbackContainer.innerHTML = '<div class="no-feedback">No feedback available yet.</div>';
            return;
        }

        feedbackContainer.innerHTML = this.feedback.map(feedback => `
            <div class="feedback-item">
                <div class="feedback-header">
                    <div class="feedback-project">
                        <h4>${feedback.projectName}</h4>
                        <span class="feedback-location">${feedback.location}</span>
                    </div>
                    <div class="feedback-rating">
                        ${this.generateStars(feedback.rating)}
                    </div>
                </div>
                <div class="feedback-content">
                    <p class="feedback-comment">${feedback.comment}</p>
                    <div class="feedback-meta">
                        <span class="feedback-user">By ${feedback.user}</span>
                        <span class="feedback-category">${feedback.category}</span>
                        <span class="feedback-status status-${feedback.status}">${feedback.status}</span>
                        <span class="feedback-date">${new Date(feedback.createdAt).toLocaleDateString()}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Generate star rating
    generateStars(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                stars += '<span class="star filled">★</span>';
            } else {
                stars += '<span class="star">☆</span>';
            }
        }
        return stars;
    }

    // Show feedback form
    showFeedbackForm(projectId = null, projectName = '') {
        const modal = document.createElement('div');
        modal.className = 'modal feedback-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Submit Feedback</h3>
                    <button onclick="this.closest('.modal').remove()" class="modal-close">×</button>
                </div>
                <form id="feedbackForm" onsubmit="feedbackSystem.handleSubmit(event)">
                    <div class="form-group">
                        <label for="projectSelect">Project (Optional)</label>
                        <select id="projectSelect" name="projectId">
                            <option value="">Select a project</option>
                            ${projectId ? `<option value="${projectId}" selected>${projectName}</option>` : ''}
                            ${projects.map(p => `<option value="${p.id}">${p.projectName}</option>`).join('')}
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="feedbackName">Your Name</label>
                        <input type="text" id="feedbackName" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="feedbackEmail">Email</label>
                        <input type="email" id="feedbackEmail" name="email" required>
                    </div>
                    <div class="form-group">
                        <label for="feedbackCategory">Category</label>
                        <select id="feedbackCategory" name="category" required>
                            <option value="">Select category</option>
                            <option value="Infrastructure">Infrastructure</option>
                            <option value="Transport">Transport</option>
                            <option value="Water Supply">Water Supply</option>
                            <option value="Housing">Housing</option>
                            <option value="Electrical">Electrical</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="feedbackRating">Rating</label>
                        <div class="rating-input">
                            <input type="radio" id="star5" name="rating" value="5">
                            <label for="star5">★</label>
                            <input type="radio" id="star4" name="rating" value="4">
                            <label for="star4">★</label>
                            <input type="radio" id="star3" name="rating" value="3">
                            <label for="star3">★</label>
                            <input type="radio" id="star2" name="rating" value="2">
                            <label for="star2">★</label>
                            <input type="radio" id="star1" name="rating" value="1">
                            <label for="star1">★</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="feedbackComment">Comment</label>
                        <textarea id="feedbackComment" name="comment" rows="4" required placeholder="Share your feedback about this project..."></textarea>
                    </div>
                    <div class="form-group">
                        <label for="feedbackLocation">Location (Optional)</label>
                        <input type="text" id="feedbackLocation" name="location" placeholder="e.g., Ward 15, Bengaluru">
                    </div>
                    <div class="form-actions">
                        <button type="button" onclick="this.closest('.modal').remove()" class="btn btn-secondary">Cancel</button>
                        <button type="submit" class="btn btn-primary">Submit Feedback</button>
                    </div>
                </form>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    // Handle feedback form submission
    async handleSubmit(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        
        const feedbackData = {
            projectId: formData.get('projectId'),
            projectName: formData.get('projectId') ? projects.find(p => p.id === formData.get('projectId'))?.projectName : '',
            user: formData.get('name'),
            email: formData.get('email'),
            category: formData.get('category'),
            rating: parseInt(formData.get('rating')),
            comment: formData.get('comment'),
            location: formData.get('location') || 'Bengaluru, Karnataka'
        };

        const result = await this.submitFeedback(feedbackData);
        
        if (result.success) {
            showNotification('Feedback submitted successfully!', 'success');
            form.closest('.modal').remove();
        } else {
            showNotification(result.error, 'error');
        }
    }
}

// Initialize feedback system
const feedbackSystem = new FeedbackSystem();

// Export for global use
window.feedbackSystem = feedbackSystem;
