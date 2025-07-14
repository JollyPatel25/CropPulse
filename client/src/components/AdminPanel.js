import React from 'react';
import '../pages/AdminPanel.css';


function AdminPanel({ user, onLogout }) {
  const token = localStorage.getItem("token");

  const postAdminRequest = async (url, label) => {
    if (!token) {
      alert("🔒 No token found. Please login again.");
      return;
    }
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });

      const data = await res.json();
      if (!res.ok) {
        const errorMessage = data.error || data.message || `Error ${res.status}`;
        alert(`❌ ${label} Failed: ${errorMessage}`);
        return;
      }

      alert(`✅ ${label}: ${data.message}`);
    } catch (err) {
      alert(`❌ Network error: ${err.message}`);
      console.error(`${label} error:`, err);
    }
  };

  return (
    <div className="admin-panel button-group">
      <h2>Admin Dashboard</h2>
      <p>Welcome, {user.username}!</p>

      <h4>🌱 Crop Recommendation</h4>
      <button onClick={() => postAdminRequest('http://localhost:5000/admin/crops/refresh-data', 'Crop Refresh')}>Refresh Crop Recommendation Dataset</button>
      <button onClick={() => postAdminRequest('http://localhost:5000/admin/crops/clean-data', 'Crop Clean')}>Clean Crop Recommendation Data</button>
      <button onClick={() => postAdminRequest('http://localhost:5000/admin/crops/train-model', 'Crop Train')}>Train Crop Recommendation Model</button><br/><br/>

      <h4>🦠 Disease Prediction</h4>
      <p style={{ color: '#666', fontSize: '0.95rem', marginTop: '-0.5rem', marginBottom: '1rem' }}>
        Note: This model uses a pretrained image classification model.
      </p>

      <h4>🌾 Fertilizer Recommendation</h4>
      <button onClick={() => postAdminRequest('http://localhost:5000/admin/fertilizer/refresh-data', 'Fertilizer Refresh')}>Refresh Fertilizer Dataset</button>
      <button onClick={() => postAdminRequest('http://localhost:5000/admin/fertilizer/clean-data', 'Fertilizer Clean')}>Clean Fertilizer Data</button>
      <button onClick={() => postAdminRequest('http://localhost:5000/admin/fertilizer/train-model', 'Fertilizer Train')}>Train Fertilizer Model</button><br/><br/>

    </div>
  );
}

export default AdminPanel;
