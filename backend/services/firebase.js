const admin = require('firebase-admin');
const serviceAccount = require('../serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://junta-d7181-default-rtdb.firebaseio.com"
});

const db = admin.firestore();
module.exports = { admin, db };