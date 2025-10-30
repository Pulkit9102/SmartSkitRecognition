import React from 'react';
import './CommonDiseasesPage.css';

const CommonDiseasesPage = () => {
  const diseases = [
    {
      name: 'Acne',
      icon: '🔴',
      description: 'A common skin condition characterized by pimples, blackheads, and inflammation.',
      symptoms: ['Pimples and pustules', 'Blackheads and whiteheads', 'Oily skin', 'Scarring'],
      causes: ['Excess oil production', 'Clogged pores', 'Bacteria', 'Hormonal changes']
    },
    {
      name: 'Eczema (Dermatitis)',
      icon: '🔥',
      description: 'An inflammatory skin condition causing itchy, red, and dry patches.',
      symptoms: ['Itchy skin', 'Red or brownish patches', 'Dry, cracked skin', 'Small raised bumps'],
      causes: ['Genetics', 'Immune system dysfunction', 'Environmental triggers', 'Irritants']
    },
    {
      name: 'Psoriasis',
      icon: '⚡',
      description: 'An autoimmune condition causing rapid skin cell buildup and scaly patches.',
      symptoms: ['Red patches with silvery scales', 'Dry, cracked skin', 'Itching and burning', 'Thickened nails'],
      causes: ['Immune system disorder', 'Genetics', 'Stress', 'Infections']
    },
    {
      name: 'Rosacea',
      icon: '🌡️',
      description: 'A chronic condition causing facial redness and visible blood vessels.',
      symptoms: ['Facial redness', 'Visible blood vessels', 'Swollen bumps', 'Eye irritation'],
      causes: ['Genetics', 'Environmental factors', 'Blood vessel abnormalities', 'Skin mites']
    },
    {
      name: 'Melanoma',
      icon: '⚫',
      description: 'The most serious type of skin cancer developing in pigment-producing cells.',
      symptoms: ['New unusual moles', 'Changes in existing moles', 'Asymmetrical spots', 'Irregular borders'],
      causes: ['UV radiation exposure', 'Genetics', 'Fair skin', 'Weakened immune system']
    },
    {
      name: 'Fungal Infections',
      icon: '🍄',
      description: 'Infections caused by fungi affecting skin, nails, or scalp.',
      symptoms: ['Itchy, scaly patches', 'Ring-shaped rashes', 'Discolored nails', 'Hair loss'],
      causes: ['Fungal spores', 'Warm, moist environments', 'Weakened immunity', 'Poor hygiene']
    }
  ];

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

      <div className="diseases-grid">
        {diseases.map((disease, index) => (
          <div key={index} className="disease-card">
            <div className="disease-header">
              <span className="disease-icon">{disease.icon}</span>
              <h2 className="disease-name">{disease.name}</h2>
            </div>
            <p className="disease-description">{disease.description}</p>
            
            <div className="disease-details">
              <div className="detail-section">
                <h3>💊 Symptoms</h3>
                <ul>
                  {disease.symptoms.map((symptom, idx) => (
                    <li key={idx}>{symptom}</li>
                  ))}
                </ul>
              </div>
              
              <div className="detail-section">
                <h3>🔬 Common Causes</h3>
                <ul>
                  {disease.causes.map((cause, idx) => (
                    <li key={idx}>{cause}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>

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
