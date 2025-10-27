// context/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for stored user session
    const storedUser = localStorage.getItem('pastPaperUser');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = async (phoneNumber, email = '') => {
    // Simulate OTP verification
    try {
      const userData = {
        id: 1,
        phoneNumber,
        email,
        role: phoneNumber === 'admin' ? 'admin' : 'student',
        subscription: null,
        createdAt: new Date().toISOString()
      };
      
      setUser(userData);
      localStorage.setItem('pastPaperUser', JSON.stringify(userData));
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('pastPaperUser');
  };

  const updateSubscription = (subscription) => {
    const updatedUser = { ...user, subscription };
    setUser(updatedUser);
    localStorage.setItem('pastPaperUser', JSON.stringify(updatedUser));
  };

  const value = {
    user,
    login,
    logout,
    updateSubscription,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};