import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

admin.initializeApp();

const db = admin.firestore();

// Export satellite inspector functions
export { satelliteInspector, triggerSatelliteAnalysis, getSatelliteAnalysis } from './satelliteInspector';

// Submit feedback with location validation
export const submitFeedback = functions.https.onCall(async (data, context) => {
  // Check if user is authenticated
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
  }

  const { projectId, comment, photoURL, rating } = data;
  const userId = context.auth.uid;

  try {
    // Get user data to validate location
    const userDoc = await db.collection('users').doc(userId).get();
    if (!userDoc.exists) {
      throw new functions.https.HttpsError('not-found', 'User not found');
    }

    const userData = userDoc.data();
    const userPincode = userData?.pincode;
    const userWard = userData?.wardInfo?.wardNumber;

    // Get project data to validate location
    const projectDoc = await db.collection('projects').doc(projectId).get();
    if (!projectDoc.exists) {
      throw new functions.https.HttpsError('not-found', 'Project not found');
    }

    const projectData = projectDoc.data();
    const projectWard = projectData?.wardNumber;

    // Validate that user's ward matches project's ward
    if (userWard && projectWard && userWard !== projectWard) {
      throw new functions.https.HttpsError(
        'permission-denied',
        'You can only provide feedback for projects in your ward'
      );
    }

    // Create feedback document
    const feedbackData = {
      comment,
      photoURL: photoURL || null,
      rating,
      timestamp: admin.firestore.FieldValue.serverTimestamp(),
      projectId,
      userId
    };

    const feedbackRef = await db.collection('userFeedback').add(feedbackData);

    return { success: true, feedbackId: feedbackRef.id };
  } catch (error) {
    console.error('Error submitting feedback:', error);
    throw new functions.https.HttpsError('internal', 'Failed to submit feedback');
  }
});

// Submit user project for crowdsourcing
export const submitUserProject = functions.https.onCall(async (data, context) => {
  // Check if user is authenticated
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
  }

  const {
    projectName,
    description,
    wardNumber,
    latitude,
    longitude,
    budget,
    department,
    startDate,
    endDate,
    contractorName,
    sourceURL
  } = data;

  const userId = context.auth.uid;

  try {
    // Validate required fields
    if (!projectName || !description || !wardNumber || !latitude || !longitude) {
      throw new functions.https.HttpsError(
        'invalid-argument',
        'Missing required fields: projectName, description, wardNumber, latitude, longitude'
      );
    }

    // Create pending project document
    const pendingProjectData = {
      projectName,
      description,
      wardNumber,
      geoPoint: new admin.firestore.GeoPoint(latitude, longitude),
      budget: budget || null,
      status: 'Pending',
      department: department || 'Unknown',
      startDate: startDate ? admin.firestore.Timestamp.fromDate(new Date(startDate)) : null,
      endDate: endDate ? admin.firestore.Timestamp.fromDate(new Date(endDate)) : null,
      contractorName: contractorName || null,
      sourceURL: sourceURL || null,
      submittedBy: userId,
      submittedAt: admin.firestore.FieldValue.serverTimestamp(),
      status: 'pending_approval'
    };

    const pendingProjectRef = await db.collection('pendingProjects').add(pendingProjectData);

    return { success: true, pendingProjectId: pendingProjectRef.id };
  } catch (error) {
    console.error('Error submitting project:', error);
    throw new functions.https.HttpsError('internal', 'Failed to submit project');
  }
});

// Get projects by ward
export const getProjectsByWard = functions.https.onCall(async (data, context) => {
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
  }

  const { wardNumber } = data;

  try {
    const projectsSnapshot = await db
      .collection('projects')
      .where('wardNumber', '==', wardNumber)
      .get();

    const projects = projectsSnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));

    return { projects };
  } catch (error) {
    console.error('Error fetching projects by ward:', error);
    throw new functions.https.HttpsError('internal', 'Failed to fetch projects');
  }
});
