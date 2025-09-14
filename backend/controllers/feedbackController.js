const { db, admin } = require('../services/firebase');

exports.submitFeedback = async (req, res) => {
  try {
    const { uid } = req.user;
    const { feedbackType, content, rating, category, projectId } = req.body;

    // Validate required fields
    if (!feedbackType || !content) {
      return res.status(400).json({ error: 'Feedback type and content are required' });
    }

    const feedbackRef = db.collection('feedback').doc();
    
    await feedbackRef.set({
      userId: uid,
      feedbackType,
      content,
      rating: rating || null,
      category: category || 'general',
      projectId: projectId || null,
      status: 'pending',
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });

    // Fetch user settings to check notification preferences
    const userSettingsRef = db.collection('userSettings').doc(uid);
    const userSettings = await userSettingsRef.get();

    if (userSettings.exists && userSettings.data().notificationPreferences?.feedbackResponses) {
      // TODO: Implement notification sending logic
      // This could be handled by a separate notification service
    }

    res.status(201).json({ 
      message: 'Feedback submitted successfully',
      feedbackId: feedbackRef.id
    });
  } catch (error) {
    console.error('Error submitting feedback:', error);
    res.status(500).json({ error: 'Failed to submit feedback' });
  }
};

exports.getUserFeedback = async (req, res) => {
  try {
    const { uid } = req.user;
    const feedbackSnapshot = await db.collection('feedback')
      .where('userId', '==', uid)
      .orderBy('createdAt', 'desc')
      .get();

    const feedback = [];
    feedbackSnapshot.forEach(doc => {
      feedback.push({
        id: doc.id,
        ...doc.data()
      });
    });

    res.json(feedback);
  } catch (error) {
    console.error('Error fetching user feedback:', error);
    res.status(500).json({ error: 'Failed to fetch feedback' });
  }
};

exports.updateFeedbackStatus = async (req, res) => {
  try {
    const { feedbackId } = req.params;
    const { status, adminResponse } = req.body;

    if (!['pending', 'in-progress', 'resolved', 'rejected'].includes(status)) {
      return res.status(400).json({ error: 'Invalid status value' });
    }

    const feedbackRef = db.collection('feedback').doc(feedbackId);
    const feedback = await feedbackRef.get();

    if (!feedback.exists) {
      return res.status(404).json({ error: 'Feedback not found' });
    }

    await feedbackRef.update({
      status,
      adminResponse: adminResponse || null,
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });

    // Check if user wants to receive notifications about feedback responses
    const userSettingsRef = db.collection('userSettings').doc(feedback.data().userId);
    const userSettings = await userSettingsRef.get();

    if (userSettings.exists && userSettings.data().notificationPreferences?.feedbackResponses) {
      // TODO: Implement notification sending logic for status updates
    }

    res.json({ message: 'Feedback status updated successfully' });
  } catch (error) {
    console.error('Error updating feedback status:', error);
    res.status(500).json({ error: 'Failed to update feedback status' });
  }
};