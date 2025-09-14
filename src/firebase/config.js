import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getFunctions } from 'firebase/functions';

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyARzOykm2wdokL7qakHUe1UI8Vz7nVZFX8",
  authDomain: "junta-d7181.firebaseapp.com",
  projectId: "junta-d7181",
  storageBucket: "junta-d7181.appspot.com",
  messagingSenderId: "939701147722",
  appId: "1:939701147722:web:cb8669135147873302aeb3",
  measurementId: "G-PZZN3RZ7G5"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);
export const functions = getFunctions(app);

export default app;
