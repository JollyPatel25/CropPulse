import React, { useState } from 'react';
import '../pages/DiseaseDetection.css';

const DiseaseDetection = () => {
  const [image, setImage] = useState(null);
  const [category, setCategory] = useState('tomato');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [previewURL, setPreviewURL] = useState(null); // 🔍 for image preview

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreviewURL(URL.createObjectURL(file)); // ✅ Show preview
    setResult('');
  };

  const handleSubmit = async () => {
    if (!image) {
      alert("Please upload an image.");
      return;
    }

    const formData = new FormData();
    formData.append('image', image);
    formData.append('category', category);

    const token = localStorage.getItem("token");

    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/disease/detect', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      const data = await res.json();
      if (res.ok) {
        setResult(`Predicted: ${data.predicted_label || `Class ${data.predicted_index}`} (${data.confidence}%)`);
      } else {
        alert(data.error || 'Prediction failed');
      }
    } catch (err) {
      console.error(err);
      alert("Network error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="disease-container">
      <h2>Plant Disease Detection</h2>

      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Detecting...' : 'Detect Disease'}
      </button>

      {result && (
        <div className="result-section">
          <h3>{result}</h3>
          {previewURL && <img src={previewURL} alt="Uploaded" className="preview-image" />}
        </div>
      )}
    </div>
  );
};

export default DiseaseDetection;
