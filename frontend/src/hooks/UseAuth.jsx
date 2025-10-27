import React, { createContext, useState, useContext, useEffect } from "react";
import { authAPI } from "../utils/api";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem("access_token"));

  useEffect(() => {
    if (token) {
      getUserProfile();
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await authAPI.login(username, password);
      const { access, refresh } = response.data;
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      setToken(access);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || "Login failed",
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || "Registration failed",
      };
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setToken(null);
    setUser(null);
  };

  const getUserProfile = async () => {
    try {
      const response = await authAPI.getProfile();
      setUser(response.data);
    } catch (error) {
      console.error("Failed to get user profile:", error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    loading,
    token,
    login,
    register,
    logout,
    getUserProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
