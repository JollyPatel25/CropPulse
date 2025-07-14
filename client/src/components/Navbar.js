// src/components/Navbar.js
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../pages/Navbar.css';
import defaultProfile from '../assets/default-profile.jpg'; // fallback image

function Navbar({ user }) {
  const location = useLocation();

  const isActive = (path) => location.pathname === path ? "active" : "";

  // profile image URL
  const imageUrl = user?.profile_image
    ? `http://localhost:5000/uploads/${user.profile_image}`
    : defaultProfile;

  // route based on role
  const profileRoute = user?.is_admin ? '/admin/profile' : '/user/profile';

  return (
    <nav className="navbar">
      <h2>CropPulse</h2>
      <div className="nav-links">
        {user ? (
          <>
            {user.is_admin ? (
              <>
                <Link to="/admin" className={isActive("/admin")}>Dashboard</Link>
                <Link to="/admin/crops" className={isActive("/admin/crops")}>Crops</Link>
                <Link to="/admin/disease" className={isActive("/admin/disease")}>Disease</Link>
                <Link to="/admin/fertilizer" className={isActive("/admin/fertilizer")}>Fertilizer</Link>
              </>
            ) : (
              <>
                <Link to="/user" className={isActive("/user")}>Dashboard</Link>
                <Link to="/user/crops" className={isActive("/user/crops")}>Crops</Link>
                <Link to="/user/disease" className={isActive("/user/disease")}>Disease</Link>
                <Link to="/user/fertilizer" className={isActive("/user/fertilizer")}>Fertilizer</Link>
              </>
            )}
            <Link to="/logout" className={isActive("/logout")}>Logout</Link>

            <div className="profile-wrapper">
              <Link to={profileRoute} className="profile-link">
                <img
                  src={imageUrl}
                  onError={(e) => { e.target.onerror = null; e.target.src = defaultProfile; }}
                  alt="Profile"
                  className="profile-image"
                />
              </Link>
            </div>
          </>
        ) : (
          <>
            <Link to="/login" className={isActive("/login")}>Login</Link>
            <Link to="/register" className={isActive("/register")}>Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
