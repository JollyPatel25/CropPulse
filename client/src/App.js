import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Login from './components/Login';
import AdminPanel from './components/AdminPanel';
import CropForm from './components/CropForm';
import Dashboard from './components/Dashboard';
import DiseaseDetection from './components/DiseaseDetection';
import ProtectedRoute from './components/ProtectedRoute';
import FertilizerPrediction from "./components/FertilizerPrediction";
import Navbar from "./components/Navbar";
import Register from './components/Register';
import MyProfile from './components/MyProfile';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

useEffect(() => {
  const token = localStorage.getItem('token');
  console.log("Token in localStorage on load:", token); 

  if (!token) {
    setLoading(false);
    return;
  }

  const verifyToken = async (retry = false) => {
    try {
      const res = await fetch('http://localhost:5000/auth/verify-token', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        }
      });

      const data = await res.json();
      console.log("/verify-token response:", data); 

      if (res.ok && data.user) {
        setUser(data.user);
        console.log("User restored:", data.user);
      } else {
        if (!retry) {
          console.warn("Verify failed, retrying in 300ms...");
          setTimeout(() => verifyToken(true), 300); // Retry once
        } else {
          console.warn("Token invalid after retry. Logging out.");
          localStorage.removeItem('token');
          setUser(null);
        }
      }
    } catch (err) {
      console.error("Token verify error:", err);
      if (!retry) {
        console.warn("Network fail. Retrying...");
        setTimeout(() => verifyToken(true), 300);
      } else {
        localStorage.removeItem('token');
        setUser(null);
      }
    } finally {
      setLoading(false);
    }
  };

  verifyToken();

}, []);


  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };
  
  const Logout = () => {
    const navigate = useNavigate();
    useEffect(() => {
      handleLogout();
      navigate('/');
    }, [navigate]);
    return <p>Logging out...</p>;
  };

  const NotFound = () => (
    <div style={{ textAlign: 'center' }}>
      <h2>404 - Page Not Found</h2>
      <p>The page you’re trying to access doesn’t exist.</p>
    </div>
  );


  if (loading) {
    return (
      <div style={{ textAlign: 'center', marginTop: '4rem' }}>
        <h2>🔄 Checking login status...</h2>
      </div>
    );
  }


  return (
    <Router>
      <Navbar user={user} />
        <Routes>
          {/* Route: Redirect root based on role */}
          <Route
            path="/"
            element={
              user ? (
                <Navigate to={user.is_admin ? "/admin" : "/user"} replace />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          {/* Login Route */}
          <Route
            path="/login"
            element={
              user ? (
                <Navigate to={user.is_admin ? "/admin" : "/user"} replace />
              ) : (
                <Login onLogin={setUser} />
              )
            }
          />
          <Route
            path="/register"
            element={
              user ? (
                <Navigate to={user.is_admin ? "/admin" : "/user"} replace />
              ) : (
                <Register onRegister={setUser} />
              )
            }
          />
          {/* Admin Routes (protected & admin-only) */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute user={user} adminOnly={true}>
                <AdminPanel user={user} onLogout={handleLogout}/>
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/crops"
            element={
              <ProtectedRoute user={user} adminOnly={true}>
                <CropForm />
              </ProtectedRoute>
            }
          />

          {/* User Routes (protected & normal users only) */}
          <Route
            path="/user"
            element={
              <ProtectedRoute user={user}>
                <Dashboard user={user} onLogout={handleLogout}/>
              </ProtectedRoute>
            }
          />
          <Route
            path="/user/crops"
            element={
              <ProtectedRoute user={user}>
                <CropForm />
              </ProtectedRoute>
            }
          />
          <Route
            path="/user/disease"
            element={
              <ProtectedRoute user={user}>
                <DiseaseDetection />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/disease"
            element={
              <ProtectedRoute user={user} adminOnly={true}>
                <DiseaseDetection />
              </ProtectedRoute>
            }
          />

          <Route
            path="/user/fertilizer"
            element={
              <ProtectedRoute user={user}>
                <FertilizerPrediction />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/fertilizer"
            element={
              <ProtectedRoute user={user} adminOnly={true}>
                <FertilizerPrediction />
              </ProtectedRoute>
            }
          />
          <Route
            path="/user/profile"
            element={
              <ProtectedRoute user={user}>
                <MyProfile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/profile"
            element={
              <ProtectedRoute user={user} adminOnly={true}>
                <MyProfile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/fertilizer"
            element={
              <ProtectedRoute user={user} adminOnly={true}>
                <MyProfile />
              </ProtectedRoute>
            }
          />
          {/* Logout */}
          <Route path="/logout" element={<Logout />} />

          {/* Fallback */}
          <Route path="*" element={<NotFound />} />
        </Routes>
    </Router>
  );
}

export default App;
