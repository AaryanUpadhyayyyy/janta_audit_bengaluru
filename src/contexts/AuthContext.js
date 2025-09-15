import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  signInWithPhoneNumber, 
  RecaptchaVerifier, 
  signOut as firebaseSignOut,
  onAuthStateChanged
} from 'firebase/auth';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { auth, db } from '../firebase/config';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [recaptchaVerifier, setRecaptchaVerifier] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        // Get user data from Firestore
        const userDoc = await getDoc(doc(db, 'users', user.uid));
        if (userDoc.exists()) {
          setCurrentUser({ ...user, ...userDoc.data() });
        } else {
          setCurrentUser(user);
        }
      } else {
        setCurrentUser(null);
      }
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const setupRecaptcha = () => {
    if (!recaptchaVerifier) {
      const verifier = new RecaptchaVerifier('recaptcha-container', {
        size: 'invisible',
        callback: (response) => {
          console.log('reCAPTCHA solved');
        },
        'expired-callback': () => {
          console.log('reCAPTCHA expired');
        }
      }, auth);
      setRecaptchaVerifier(verifier);
    }
    return recaptchaVerifier;
  };

  const signInWithPhone = async (phoneNumber) => {
    try {
      const verifier = setupRecaptcha();
      const confirmationResult = await signInWithPhoneNumber(auth, phoneNumber, verifier);
      return confirmationResult;
    } catch (error) {
      console.error('Error sending OTP:', error);
      throw error;
    }
  };

  const verifyOTP = async (confirmationResult, otp) => {
    try {
      const result = await confirmationResult.confirm(otp);
      return result;
    } catch (error) {
      console.error('Error verifying OTP:', error);
      throw error;
    }
  };

  const createUserProfile = async (user, userData) => {
    try {
      await setDoc(doc(db, 'users', user.uid), {
        mobileNumber: user.phoneNumber,
        pincode: userData.pincode,
        wardInfo: userData.wardInfo,
        createdAt: new Date()
      });
    } catch (error) {
      console.error('Error creating user profile:', error);
      throw error;
    }
  };

  const signOut = async () => {
    try {
      await firebaseSignOut(auth);
    } catch (error) {
      console.error('Error signing out:', error);
      throw error;
    }
  };

  const value = {
    currentUser,
    loading,
    signInWithPhone,
    verifyOTP,
    createUserProfile,
    signOut
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
