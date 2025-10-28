import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/UseAuth";
import Loader from "./Loader";

const ProtectedRoute = ({ children, requireSubscription = false }) => {
  const { user, loading, token } = useAuth();
  const location = useLocation();

  if (loading) {
    return <Loader text="Checking authentication..." />;
  }

  if (!token || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requireSubscription && !user.hasActiveSubscription) {
    return <Navigate to="/subscription" state={{ from: location }} replace />;
  }

  return children;
};

export default ProtectedRoute;
