const functions = require('firebase-functions');
const admin = require('firebase-admin');

// Initialize Firebase Admin SDK
admin.initializeApp();
const db = admin.firestore();

/**
 * Cloud Function to handle follow/unfollow operations
 * This function manages the social follow system with atomic transactions
 * to ensure data consistency across multiple documents and subcollections.
 */
exports.updateFollowStatus = functions.https.onCall(async (data, context) => {
    // Get the follower (current user) and followed user IDs
    const followerId = context.auth.uid;
    const followedId = data.targetUserId;

    // Validate authentication
    if (!followerId) {
        throw new functions.https.HttpsError('unauthenticated', 'User must be logged in to follow.');
    }

    // Prevent self-following
    if (followerId === followedId) {
        throw new functions.https.HttpsError('invalid-argument', 'A user cannot follow themselves.');
    }

    // Validate that targetUserId is provided
    if (!followedId) {
        throw new functions.https.HttpsError('invalid-argument', 'Target user ID is required.');
    }

    // Set up document references
    const followerRef = db.collection('users').doc(followerId);
    const followedRef = db.collection('users').doc(followedId);
    const followingDocRef = followerRef.collection('following').doc(followedId);

    try {
        // Use Firestore transaction to ensure atomicity
        const result = await db.runTransaction(async (transaction) => {
            // Check if the relationship already exists
            const followingDoc = await transaction.get(followingDocRef);
            
            // Verify both users exist
            const followerDoc = await transaction.get(followerRef);
            const followedDoc = await transaction.get(followedRef);
            
            if (!followerDoc.exists) {
                throw new functions.https.HttpsError('not-found', 'Follower user not found.');
            }
            
            if (!followedDoc.exists) {
                throw new functions.https.HttpsError('not-found', 'Target user not found.');
            }

            if (followingDoc.exists) {
                // --- UNFOLLOW LOGIC ---
                console.log(`Unfollowing: ${followerId} -> ${followedId}`);
                
                // 1. Remove from follower's "following" subcollection
                transaction.delete(followerRef.collection('following').doc(followedId));
                
                // 2. Remove follower from target's "followers" subcollection
                transaction.delete(followedRef.collection('followers').doc(followerId));
                
                // 3. Decrement counts atomically
                transaction.update(followerRef, { 
                    followingCount: admin.firestore.FieldValue.increment(-1) 
                });
                transaction.update(followedRef, { 
                    followersCount: admin.firestore.FieldValue.increment(-1) 
                });
                
                return { status: 'unfollowed' };
            } else {
                // --- FOLLOW LOGIC ---
                console.log(`Following: ${followerId} -> ${followedId}`);
                
                // 1. Add to follower's "following" subcollection
                transaction.set(followerRef.collection('following').doc(followedId), { 
                    timestamp: admin.firestore.FieldValue.serverTimestamp(),
                    userId: followedId
                });
                
                // 2. Add follower to target's "followers" subcollection
                transaction.set(followedRef.collection('followers').doc(followerId), { 
                    timestamp: admin.firestore.FieldValue.serverTimestamp(),
                    userId: followerId
                });
                
                // 3. Increment counts atomically
                transaction.update(followerRef, { 
                    followingCount: admin.firestore.FieldValue.increment(1) 
                });
                transaction.update(followedRef, { 
                    followersCount: admin.firestore.FieldValue.increment(1) 
                });
                
                return { status: 'followed' };
            }
        });

        console.log(`Follow operation completed: ${result.status}`);
        return result;

    } catch (error) {
        console.error('Error in updateFollowStatus transaction:', error);
        
        // Handle specific error types
        if (error instanceof functions.https.HttpsError) {
            throw error; // Re-throw HttpsError as-is
        }
        
        // Handle Firestore errors
        throw new functions.https.HttpsError('internal', 'Failed to update follow status.');
    }
});

/**
 * Cloud Function to get user's follower statistics
 * This is a helper function for retrieving follower/following counts
 */
exports.getUserFollowStats = functions.https.onCall(async (data, context) => {
    const userId = data.userId || context.auth.uid;

    if (!userId) {
        throw new functions.https.HttpsError('invalid-argument', 'User ID is required.');
    }

    try {
        const userDoc = await db.collection('users').doc(userId).get();
        
        if (!userDoc.exists) {
            throw new functions.https.HttpsError('not-found', 'User not found.');
        }

        const userData = userDoc.data();
        
        return {
            followersCount: userData.followersCount || 0,
            followingCount: userData.followingCount || 0
        };

    } catch (error) {
        console.error('Error getting user follow stats:', error);
        
        if (error instanceof functions.https.HttpsError) {
            throw error;
        }
        
        throw new functions.https.HttpsError('internal', 'Failed to get user stats.');
    }
});

/**
 * Cloud Function to check if user A follows user B
 * This is a helper function for UI state management
 */
exports.checkFollowStatus = functions.https.onCall(async (data, context) => {
    const followerId = context.auth.uid;
    const targetUserId = data.targetUserId;

    if (!followerId) {
        throw new functions.https.HttpsError('unauthenticated', 'User must be logged in.');
    }

    if (!targetUserId) {
        throw new functions.https.HttpsError('invalid-argument', 'Target user ID is required.');
    }

    try {
        const followingDoc = await db
            .collection('users')
            .doc(followerId)
            .collection('following')
            .doc(targetUserId)
            .get();

        return {
            isFollowing: followingDoc.exists
        };

    } catch (error) {
        console.error('Error checking follow status:', error);
        throw new functions.https.HttpsError('internal', 'Failed to check follow status.');
    }
});

/**
 * Trigger function to maintain data consistency
 * This runs whenever a user document is created to ensure proper initialization
 */
exports.onUserCreate = functions.firestore
    .document('users/{userId}')
    .onCreate(async (snap, context) => {
        const userData = snap.data();
        const userId = context.params.userId;

        // Ensure follower counts are initialized
        if (userData.followersCount === undefined || userData.followingCount === undefined) {
            try {
                await snap.ref.update({
                    followersCount: userData.followersCount || 0,
                    followingCount: userData.followingCount || 0
                });
                console.log(`Initialized follow counts for user: ${userId}`);
            } catch (error) {
                console.error(`Error initializing follow counts for user ${userId}:`, error);
            }
        }
    });

/**
 * Scheduled function to periodically verify and fix inconsistent follower counts
 * This runs daily to ensure data integrity
 */
exports.syncFollowerCounts = functions.pubsub
    .schedule('0 2 * * *') // Run at 2 AM daily
    .timeZone('Asia/Kolkata')
    .onRun(async (context) => {
        console.log('Starting follower count synchronization...');
        
        try {
            const usersSnapshot = await db.collection('users').get();
            const batch = db.batch();
            let updatedCount = 0;

            for (const userDoc of usersSnapshot.docs) {
                const userId = userDoc.id;
                
                // Count actual followers and following
                const [followersSnapshot, followingSnapshot] = await Promise.all([
                    db.collection('users').doc(userId).collection('followers').get(),
                    db.collection('users').doc(userId).collection('following').get()
                ]);

                const actualFollowersCount = followersSnapshot.size;
                const actualFollowingCount = followingSnapshot.size;
                
                const userData = userDoc.data();
                const storedFollowersCount = userData.followersCount || 0;
                const storedFollowingCount = userData.followingCount || 0;

                // Update if counts don't match
                if (actualFollowersCount !== storedFollowersCount || 
                    actualFollowingCount !== storedFollowingCount) {
                    
                    batch.update(userDoc.ref, {
                        followersCount: actualFollowersCount,
                        followingCount: actualFollowingCount
                    });
                    
                    updatedCount++;
                    console.log(`Updated counts for user ${userId}: ` +
                        `followers ${storedFollowersCount} -> ${actualFollowersCount}, ` +
                        `following ${storedFollowingCount} -> ${actualFollowingCount}`);
                }
            }

            if (updatedCount > 0) {
                await batch.commit();
                console.log(`Synchronized ${updatedCount} user follower counts`);
            } else {
                console.log('All follower counts are already synchronized');
            }

        } catch (error) {
            console.error('Error during follower count synchronization:', error);
        }
    });
