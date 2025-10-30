import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Loader from "./Loader";

const ProtectedRoute = ({ children, requireSubscription = false }) => {
  const { user, loading, token } = useAuth();
  const location = useLocation();

  if (loading) return <Loader text="Checking authentication..." />;

  // Not logged in
  if (!token || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Subscription check
  if (requireSubscription && !user.hasActiveSubscription) {
    return <Navigate to="/subscription" state={{ from: location }} replace />;
  }

  return children;
};

export default ProtectedRoute;
