import React, { useState } from 'react';
import '../pages/CropForm.css';

function CropForm() {
  const [inputs, setInputs] = useState({
    N: '', P: '', K: '', temperature: '', humidity: '', ph: '', rainfall: ''
  });
  const [result, setResult] = useState([]);
  const [error, setError] = useState('');

  const handleChange = e => {
    const { name, value } = e.target;
    setInputs(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    setResult([]);
    setError('');

    for (let key in inputs) {
      if (inputs[key] === '') {
        setError(`Please fill in ${key}`);
        return;
      }
    }

    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:5000/recommend/crop', {
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
      setError('Network error: ' + err.message);
    }
  };

  // Map of param to readable label
  const fieldLabels = {
    N: 'Nitrogen (N)',
    P: 'Phosphorus (P)',
    K: 'Potassium (K)',
    temperature: 'Temperature (°C)',
    humidity: 'Humidity (%)',
    ph: 'Soil pH',
    rainfall: 'Rainfall (mm)'
  };

  return (
    <div className="crop-page">
      <div className="crop-form-container">
        <h2>🌱 Crop Recommendation</h2>
        <div className="crop-form">
          {Object.keys(inputs).map(param => (
            <div className="form-group" key={param}>
              <label htmlFor={param}>{fieldLabels[param]}</label>
              <input
                name={param}
                id={param}
                type="number"
                value={inputs[param]}
                onChange={handleChange}
                step="any"
              />
            </div>
          ))}
          <button onClick={handleSubmit}>Recommend Crop</button>
        </div>
        
        {error && <p className="error-msg">{error}</p>}
      </div>

      {result.length > 0 && (
        <div className="result-box">
          <h3>✅ Top Crop Recommendations</h3>
          <ul>
            {result.map((item, index) => (
              <li key={index}>
                {index + 1}. <strong>{item.crop.charAt(0).toUpperCase() + item.crop.slice(1)}</strong> — {item.confidence}% confidence
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default CropForm;
