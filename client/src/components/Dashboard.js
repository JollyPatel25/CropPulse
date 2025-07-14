import React from 'react';
import { Navigate } from 'react-router-dom';
import '../pages/UserDashboard.css'; // Optional if you want styling

const Dashboard = ({ user }) => {
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="user-dashboard">
      <h2>Welcome, {user.username}</h2>

      <div className="dashboard-section">
        <h3>🌱 Crop Recommendation</h3>
        <p>
          This module helps you identify the most suitable crop to grow based on local environmental conditions such as soil nutrients (NPK), temperature, humidity, pH, and rainfall. The system uses a machine learning model trained on agricultural datasets to make scientifically informed suggestions.
        </p>
      </div>

      <div className="dashboard-section">
        <h3>🦠 Disease Detection</h3>
        <p>
          The disease prediction system allows you to upload images of plant leaves to detect potential diseases. It uses a <strong>pretrained deep learning image classification model</strong> trained on the PlantVillage dataset to identify diseases affecting crops like tomato, maize, cabbage, and soybean.
        </p>
      </div>

      <div className="dashboard-section">
        <h3>💧 Fertilizer Recommendation</h3>
        <p>
          This module analyzes your soil data (NPK levels) and crop type to suggest the most suitable fertilizer. It helps optimize nutrient balance, reduce costs, and improve productivity. The model is trained on a curated fertilizer dataset to give accurate and tailored suggestions.
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
