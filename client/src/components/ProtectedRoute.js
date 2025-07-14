import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ user, children, adminOnly = false }) => {
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && !user.is_admin) {
    return <Navigate to="/user" replace />;
  }

  if (!adminOnly && user.is_admin) {
    return <Navigate to="/admin" replace />;
  }

  return children;
};

export default ProtectedRoute;
