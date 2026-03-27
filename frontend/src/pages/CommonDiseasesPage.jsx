import React, { useState, useEffect } from 'react';
import './CommonDiseasesPage.css';
import apiService from '../services/apiService';

const CommonDiseasesPage = () => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    apiService.getClasses()
      .then((data) => {
        setClasses(Array.isArray(data) ? data : data.classes || []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="common-diseases-page">
      <div className="page-header">
        <h1 className="page-title">
          <span className="title-icon">📋</span>
          Common Skin Diseases
        </h1>
        <p className="page-description">
          Learn about the most prevalent skin conditions, their symptoms, and causes
        </p>
      </div>

      {loading && <p style={{ textAlign: 'center' }}>Loading diseases...</p>}
      {error && <p style={{ textAlign: 'center', color: '#b91c1c' }}>Could not load diseases: {error}</p>}

      {!loading && !error && (
        <div className="diseases-grid">
          {classes.map((name, index) => (
            <div key={index} className="disease-card">
              <div className="disease-header">
                <h2 className="disease-name">{name}</h2>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="disclaimer-box">
        <strong>⚠️ Medical Disclaimer</strong>
        <p>
          This information is for educational purposes only. Always consult with a qualified
          healthcare professional for proper diagnosis and treatment of skin conditions.
        </p>
      </div>
    </div>
  );
};

export default CommonDiseasesPage;
