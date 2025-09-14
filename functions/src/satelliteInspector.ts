import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
import { spawn } from 'child_process';
import * as path from 'path';

// Initialize Firebase Admin (if not already initialized)
if (!admin.apps.length) {
  admin.initializeApp();
}

const db = admin.firestore();

/**
 * Cloud Function triggered by Firestore document changes in projects collection
 * Automatically runs satellite analysis when projects are created or status is updated
 */
export const satelliteInspector = functions.firestore
  .document('projects/{projectId}')
  .onWrite(async (change, context) => {
    const projectId = context.params.projectId;
    const before = change.before;
    const after = change.after;

    // Check if this is a new document or status update
    const isNewDocument = !before.exists;
    const isStatusUpdate = before.exists && after.exists && 
      before.data()?.status !== after.data()?.status;

    if (!isNewDocument && !isStatusUpdate) {
      console.log(`No relevant changes detected for project ${projectId}`);
      return null;
    }

    const projectData = after.data();
    if (!projectData) {
      console.log(`No project data found for ${projectId}`);
      return null;
    }

    // Check if project has required geoPoint data
    if (!projectData.geoPoint || !projectData.geoPoint.latitude || !projectData.geoPoint.longitude) {
      console.log(`Project ${projectId} missing geoPoint data, skipping satellite analysis`);
      return null;
    }

    console.log(`Triggering satellite analysis for project ${projectId}: ${projectData.projectName}`);

    try {
      // Run the satellite inspector Python script
      await runSatelliteAnalysis(projectId, projectData);
      
      console.log(`Satellite analysis completed for project ${projectId}`);
      return null;
    } catch (error) {
      console.error(`Error running satellite analysis for project ${projectId}:`, error);
      
      // Log error to Firestore for debugging
      await db.collection('satelliteAnalysisLogs').add({
        projectId,
        error: error.message,
        timestamp: admin.firestore.FieldValue.serverTimestamp(),
        status: 'failed'
      });
      
      return null;
    }
  });

/**
 * Run the satellite analysis Python script
 */
async function runSatelliteAnalysis(projectId: string, projectData: any): Promise<void> {
  return new Promise((resolve, reject) => {
    const pythonScriptPath = path.join(__dirname, '../../python_scripts/satellite_inspector.py');
    
    // Prepare project data for Python script
    const projectDataForPython = {
      projectId,
      projectName: projectData.projectName,
      geoPoint: projectData.geoPoint,
      status: projectData.status,
      startDate: projectData.startDate,
      endDate: projectData.endDate,
      department: projectData.department,
      wardNumber: projectData.wardNumber
    };

    // Spawn Python process
    const pythonProcess = spawn('python3', [pythonScriptPath], {
      cwd: path.join(__dirname, '../../python_scripts'),
      env: {
        ...process.env,
        PROJECT_DATA: JSON.stringify(projectDataForPython)
      }
    });

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
      console.log(`Python stdout: ${data.toString()}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
      console.error(`Python stderr: ${data.toString()}`);
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        console.log(`Satellite analysis completed successfully for project ${projectId}`);
        resolve();
      } else {
        console.error(`Satellite analysis failed for project ${projectId} with code ${code}`);
        console.error(`stderr: ${stderr}`);
        reject(new Error(`Python script failed with code ${code}: ${stderr}`));
      }
    });

    pythonProcess.on('error', (error) => {
      console.error(`Failed to start satellite analysis for project ${projectId}:`, error);
      reject(error);
    });

    // Set timeout for the Python process (10 minutes)
    setTimeout(() => {
      pythonProcess.kill();
      reject(new Error('Satellite analysis timed out after 10 minutes'));
    }, 10 * 60 * 1000);
  });
}

/**
 * Manual trigger function for satellite analysis
 * Can be called via HTTP to manually trigger analysis for specific projects
 */
export const triggerSatelliteAnalysis = functions.https.onCall(async (data, context) => {
  // Check if user is authenticated
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
  }

  const { projectId } = data;
  if (!projectId) {
    throw new functions.https.HttpsError('invalid-argument', 'Project ID is required');
  }

  try {
    // Get project data
    const projectDoc = await db.collection('projects').doc(projectId).get();
    if (!projectDoc.exists) {
      throw new functions.https.HttpsError('not-found', 'Project not found');
    }

    const projectData = projectDoc.data();
    if (!projectData) {
      throw new functions.https.HttpsError('not-found', 'Project data not found');
    }

    // Run satellite analysis
    await runSatelliteAnalysis(projectId, projectData);

    return {
      success: true,
      message: `Satellite analysis triggered for project ${projectId}`,
      projectId
    };
  } catch (error) {
    console.error(`Error in manual satellite analysis trigger:`, error);
    throw new functions.https.HttpsError('internal', 'Failed to trigger satellite analysis');
  }
});

/**
 * Get satellite analysis results for a project
 */
export const getSatelliteAnalysis = functions.https.onCall(async (data, context) => {
  // Check if user is authenticated
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
  }

  const { projectId } = data;
  if (!projectId) {
    throw new functions.https.HttpsError('invalid-argument', 'Project ID is required');
  }

  try {
    // Get project data
    const projectDoc = await db.collection('projects').doc(projectId).get();
    if (!projectDoc.exists) {
      throw new functions.https.HttpsError('not-found', 'Project not found');
    }

    const projectData = projectDoc.data();
    if (!projectData) {
      throw new functions.https.HttpsError('not-found', 'Project data not found');
    }

    // Return satellite analysis if available
    const satelliteAnalysis = projectData.satelliteAnalysis;
    if (!satelliteAnalysis) {
      return {
        success: false,
        message: 'No satellite analysis available for this project'
      };
    }

    return {
      success: true,
      analysis: satelliteAnalysis
    };
  } catch (error) {
    console.error(`Error getting satellite analysis:`, error);
    throw new functions.https.HttpsError('internal', 'Failed to get satellite analysis');
  }
});
