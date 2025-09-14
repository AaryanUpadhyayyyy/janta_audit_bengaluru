const { db, admin } = require('../services/firebase');

exports.updateUserSettings = async (req, res) => {
  try {
    const { uid } = req.user;
    const {
      firstName,
      lastName,
      email,
      phoneNumber,
      organization,
      bio,
      notificationPreferences,
      privacySettings
    } = req.body;

    const userSettingsRef = db.collection('userSettings').doc(uid);
    
    await userSettingsRef.set({
      firstName,
      lastName,
      email,
      phoneNumber,
      organization,
      bio,
      notificationPreferences: notificationPreferences || {
        email: true,
        sms: false,
        projectUpdates: true,
        feedbackResponses: true
      },
      privacySettings: privacySettings || {
        profileVisibility: 'public',
        showEmail: false,
        showPhone: false
      },
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    }, { merge: true });

    const updatedSettings = await userSettingsRef.get();
    res.json(updatedSettings.data());
  } catch (error) {
    console.error('Error updating settings:', error);
    res.status(500).json({ error: 'Failed to update settings' });
  }
};

exports.getUserSettings = async (req, res) => {
  try {
    const { uid } = req.user;
    const userSettingsRef = db.collection('userSettings').doc(uid);
    const doc = await userSettingsRef.get();

    if (!doc.exists) {
      return res.json({
        notificationPreferences: {
          email: true,
          sms: false,
          projectUpdates: true,
          feedbackResponses: true
        },
        privacySettings: {
          profileVisibility: 'public',
          showEmail: false,
          showPhone: false
        }
      });
    }

    res.json(doc.data());
  } catch (error) {
    console.error('Error getting settings:', error);
    res.status(500).json({ error: 'Failed to fetch settings' });
  }
};