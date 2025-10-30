import React, { createContext, useState, useContext, useEffect } from "react";
import { authAPI } from "../utils/api";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null); // expose access_token
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem("pastPaperUser");
    const storedToken = localStorage.getItem("access_token");
    if (storedUser) setUser(JSON.parse(storedUser));
    if (storedToken) setToken(storedToken);
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await authAPI.login(username, password);
      const { access_token, refresh_token } = response.data;

      if (!access_token || !refresh_token) {
        return { success: false, error: "Invalid credentials" };
      }

      // Save tokens
      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);
      setToken(access_token);

      // Fetch user profile
      const profileRes = await authAPI.getProfile();
      const userData = profileRes.data;
      setUser(userData);
      localStorage.setItem("pastPaperUser", JSON.stringify(userData));

      return { success: true };
    } catch (err) {
      return {
        success: false,
        error: err.response?.data?.detail || err.message,
      };
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("pastPaperUser");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  };

  const value = { user, token, login, logout, loading };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
