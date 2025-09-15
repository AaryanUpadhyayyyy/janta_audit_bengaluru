import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { MapPin, Phone, ArrowRight } from 'lucide-react';

const Login = () => {
  const navigate = useNavigate();
  const { currentUser, signInWithPhone, verifyOTP, createUserProfile, loading: authLoading } = useAuth();
  const [step, setStep] = useState('phone'); // 'phone', 'otp', 'profile'
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState('');
  const [confirmationResult, setConfirmationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [userProfile, setUserProfile] = useState({
    pincode: '',
    wardNumber: ''
  });

  useEffect(() => {
    if (currentUser) {
      navigate('/');
    }
  }, [currentUser, navigate]);

  // Handle loading state
  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        <span className="ml-2 text-gray-600">Loading...</span>
      </div>
    );
  }

  const handlePhoneSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const formattedPhone = phoneNumber.startsWith('+91') ? phoneNumber : `+91${phoneNumber}`;
      const result = await signInWithPhone(formattedPhone);
      setConfirmationResult(result);
      setStep('otp');
    } catch (error) {
      setError('Failed to send OTP. Please try again.');
      console.error('Error sending OTP:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleOTPSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const result = await verifyOTP(confirmationResult, otp);
      if (result.user) {
        setStep('profile');
      }
    } catch (error) {
      setError('Invalid OTP. Please try again.');
      console.error('Error verifying OTP:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await createUserProfile(currentUser, {
        pincode: userProfile.pincode,
        wardInfo: {
          wardNumber: userProfile.wardNumber
        }
      });
      navigate('/');
    } catch (error) {
      setError('Failed to create profile. Please try again.');
      console.error('Error creating profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const bengaluruWards = [
    'Ward 1', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6', 'Ward 7', 'Ward 8',
    'Ward 9', 'Ward 10', 'Ward 11', 'Ward 12', 'Ward 13', 'Ward 14', 'Ward 15', 'Ward 16',
    'Ward 17', 'Ward 18', 'Ward 19', 'Ward 20', 'Ward 21', 'Ward 22', 'Ward 23', 'Ward 24',
    'Ward 25', 'Ward 26', 'Ward 27', 'Ward 28', 'Ward 29', 'Ward 30', 'Ward 31', 'Ward 32',
    'Ward 33', 'Ward 34', 'Ward 35', 'Ward 36', 'Ward 37', 'Ward 38', 'Ward 39', 'Ward 40',
    'Ward 41', 'Ward 42', 'Ward 43', 'Ward 44', 'Ward 45', 'Ward 46', 'Ward 47', 'Ward 48',
    'Ward 49', 'Ward 50', 'Ward 51', 'Ward 52', 'Ward 53', 'Ward 54', 'Ward 55', 'Ward 56',
    'Ward 57', 'Ward 58', 'Ward 59', 'Ward 60', 'Ward 61', 'Ward 62', 'Ward 63', 'Ward 64',
    'Ward 65', 'Ward 66', 'Ward 67', 'Ward 68', 'Ward 69', 'Ward 70', 'Ward 71', 'Ward 72',
    'Ward 73', 'Ward 74', 'Ward 75', 'Ward 76', 'Ward 77', 'Ward 78', 'Ward 79', 'Ward 80',
    'Ward 81', 'Ward 82', 'Ward 83', 'Ward 84', 'Ward 85', 'Ward 86', 'Ward 87', 'Ward 88',
    'Ward 89', 'Ward 90', 'Ward 91', 'Ward 92', 'Ward 93', 'Ward 94', 'Ward 95', 'Ward 96',
    'Ward 97', 'Ward 98', 'Ward 99', 'Ward 100', 'Ward 101', 'Ward 102', 'Ward 103', 'Ward 104',
    'Ward 105', 'Ward 106', 'Ward 107', 'Ward 108', 'Ward 109', 'Ward 110', 'Ward 111', 'Ward 112',
    'Ward 113', 'Ward 114', 'Ward 115', 'Ward 116', 'Ward 117', 'Ward 118', 'Ward 119', 'Ward 120',
    'Ward 121', 'Ward 122', 'Ward 123', 'Ward 124', 'Ward 125', 'Ward 126', 'Ward 127', 'Ward 128',
    'Ward 129', 'Ward 130', 'Ward 131', 'Ward 132', 'Ward 133', 'Ward 134', 'Ward 135', 'Ward 136',
    'Ward 137', 'Ward 138', 'Ward 139', 'Ward 140', 'Ward 141', 'Ward 142', 'Ward 143', 'Ward 144',
    'Ward 145', 'Ward 146', 'Ward 147', 'Ward 148', 'Ward 149', 'Ward 150', 'Ward 151', 'Ward 152',
    'Ward 153', 'Ward 154', 'Ward 155', 'Ward 156', 'Ward 157', 'Ward 158', 'Ward 159', 'Ward 160',
    'Ward 161', 'Ward 162', 'Ward 163', 'Ward 164', 'Ward 165', 'Ward 166', 'Ward 167', 'Ward 168',
    'Ward 169', 'Ward 170', 'Ward 171', 'Ward 172', 'Ward 173', 'Ward 174', 'Ward 175', 'Ward 176',
    'Ward 177', 'Ward 178', 'Ward 179', 'Ward 180', 'Ward 181', 'Ward 182', 'Ward 183', 'Ward 184',
    'Ward 185', 'Ward 186', 'Ward 187', 'Ward 188', 'Ward 189', 'Ward 190', 'Ward 191', 'Ward 192',
    'Ward 193', 'Ward 194', 'Ward 195', 'Ward 196', 'Ward 197', 'Ward 198', 'Ward 199', 'Ward 200'
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex justify-center">
            <MapPin className="h-12 w-12 text-blue-600" />
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900">
            Janata Audit Bengaluru
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Sign in to track civic projects and provide feedback
          </p>
        </div>

        {/* reCAPTCHA Container */}
        <div id="recaptcha-container"></div>

        {/* Phone Number Step */}
        {step === 'phone' && (
          <form className="mt-8 space-y-6" onSubmit={handlePhoneSubmit}>
            <div className="bg-white py-8 px-6 shadow rounded-lg">
              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Phone className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="phone"
                    name="phone"
                    type="tel"
                    required
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    className="appearance-none relative block w-full pl-10 pr-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                    placeholder="Enter your phone number"
                  />
                </div>
                <p className="mt-1 text-xs text-gray-500">
                  We'll send you a verification code via SMS
                </p>
              </div>

              {error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-600">{error}</p>
                </div>
              )}

              <div className="mt-6">
                <button
                  type="submit"
                  disabled={loading}
                  className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <div className="loading-spinner"></div>
                  ) : (
                    <>
                      Send OTP
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </>
                  )}
                </button>
              </div>
            </div>
          </form>
        )}

        {/* OTP Verification Step */}
        {step === 'otp' && (
          <form className="mt-8 space-y-6" onSubmit={handleOTPSubmit}>
            <div className="bg-white py-8 px-6 shadow rounded-lg">
              <div>
                <label htmlFor="otp" className="block text-sm font-medium text-gray-700 mb-2">
                  Verification Code
                </label>
                <input
                  id="otp"
                  name="otp"
                  type="text"
                  required
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter 6-digit code"
                  maxLength="6"
                />
                <p className="mt-1 text-xs text-gray-500">
                  Enter the 6-digit code sent to {phoneNumber}
                </p>
              </div>

              {error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-600">{error}</p>
                </div>
              )}

              <div className="mt-6">
                <button
                  type="submit"
                  disabled={loading}
                  className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <div className="loading-spinner"></div>
                  ) : (
                    'Verify OTP'
                  )}
                </button>
              </div>

              <div className="mt-4 text-center">
                <button
                  type="button"
                  onClick={() => setStep('phone')}
                  className="text-sm text-blue-600 hover:text-blue-500"
                >
                  Change phone number
                </button>
              </div>
            </div>
          </form>
        )}

        {/* Profile Setup Step */}
        {step === 'profile' && (
          <form className="mt-8 space-y-6" onSubmit={handleProfileSubmit}>
            <div className="bg-white py-8 px-6 shadow rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-6">
                Complete Your Profile
              </h3>

              <div className="space-y-4">
                <div>
                  <label htmlFor="pincode" className="block text-sm font-medium text-gray-700 mb-2">
                    Pincode
                  </label>
                  <input
                    id="pincode"
                    name="pincode"
                    type="text"
                    required
                    value={userProfile.pincode}
                    onChange={(e) => setUserProfile({ ...userProfile, pincode: e.target.value })}
                    className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder="Enter your pincode"
                    maxLength="6"
                  />
                </div>

                <div>
                  <label htmlFor="ward" className="block text-sm font-medium text-gray-700 mb-2">
                    BBMP Ward
                  </label>
                  <select
                    id="ward"
                    name="ward"
                    required
                    value={userProfile.wardNumber}
                    onChange={(e) => setUserProfile({ ...userProfile, wardNumber: e.target.value })}
                    className="appearance-none relative block w-full px-3 py-2 border border-gray-300 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  >
                    <option value="">Select your ward</option>
                    {bengaluruWards.map((ward) => (
                      <option key={ward} value={ward}>
                        {ward}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-600">{error}</p>
                </div>
              )}

              <div className="mt-6">
                <button
                  type="submit"
                  disabled={loading}
                  className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <div className="loading-spinner"></div>
                  ) : (
                    'Complete Setup'
                  )}
                </button>
              </div>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default Login;
