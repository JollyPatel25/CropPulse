import React, { useState } from 'react';
import "../pages/FertilizerPrediction.css";

function FertilizerPrediction() {
  const [inputs, setInputs] = useState({
    Temperature: '', Humidity: '', Moisture: '',
    Nitrogen: '', Potassium: '', Phosphorous: '',
    "Soil Type": '', "Crop Type": ''
  });
  const [result, setResult] = useState([]);
  const [error, setError] = useState('');

  const soilTypes = ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey'];
  const cropTypes = [
    'Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Barley', 'Wheat',
    'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts'
  ];

  const handleChange = e => {
    const { name, value } = e.target;
    setInputs(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    setResult([]);
    setError('');

    for (let key in inputs) {
      if (inputs[key] === '') {
        setError(`❌ Please fill in ${key}`);
        return;
      }
    }

    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:5000/fertilizer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(inputs)
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.message || data.error || 'Server error');
      } else {
        setResult(data.top_recommendations || []);
      }
    } catch (err) {
      setError('🚨 Network error: ' + err.message);
    }
  };

  return (
    <div className={`fertilizer-page ${result.length === 0 ? "centered" : ""}`}>
      <div className="fertilizer-form-container">
        <h2> Fertilizer Recommendation</h2>
        <div className="form-grid">
          {['Temperature', 'Humidity', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous'].map(param => (
            <div className="form-group" key={param}>
              <label>{param}</label>
              <input
                name={param}
                type="number"
                value={inputs[param]}
                onChange={handleChange}
                step="any"
              />
            </div>
          ))}

          <div className="form-group">
            <label>Soil Type</label>
            <select name="Soil Type" value={inputs["Soil Type"]} onChange={handleChange}>
              <option value="">Select Soil Type</option>
              {soilTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Crop Type</label>
            <select name="Crop Type" value={inputs["Crop Type"]} onChange={handleChange}>
              <option value="">Select Crop Type</option>
              {cropTypes.map(crop => (
                <option key={crop} value={crop}>{crop}</option>
              ))}
            </select>
          </div>
        </div>

        <button className="fertilizer-button" onClick={handleSubmit}>
          Recommend Fertilizer
        </button>

        {error && <p className="error-message">{error}</p>}
      </div>

      {result.length > 0 && (
        <div className="fertilizer-result-container">
          <h3> Top Fertilizer Recommendations</h3>
          <ul>
            {result.map((item, index) => (
              <li key={index}>
                {index + 1}. <strong>{item.fertilizer}</strong> — {item.confidence}% confidence
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default FertilizerPrediction;
