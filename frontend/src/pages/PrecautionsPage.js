import React from 'react';
import './PrecautionsPage.css';

const PrecautionsPage = () => {
  const precautionCategories = [
    {
      title: 'Daily Skin Care',
      icon: '🧴',
      tips: [
        'Cleanse your skin twice daily with a gentle, pH-balanced cleanser',
        'Apply moisturizer suitable for your skin type every day',
        'Use sunscreen with at least SPF 30, even on cloudy days',
        'Remove makeup before sleeping to prevent clogged pores',
        'Stay hydrated by drinking at least 8 glasses of water daily'
      ]
    },
    {
      title: 'Sun Protection',
      icon: '☀️',
      tips: [
        'Wear protective clothing including wide-brimmed hats',
        'Seek shade during peak sun hours (10 AM - 4 PM)',
        'Reapply sunscreen every 2 hours when outdoors',
        'Use sunglasses to protect the delicate skin around your eyes',
        'Avoid tanning beds and prolonged sun exposure'
      ]
    },
    {
      title: 'Hygiene Practices',
      icon: '🧼',
      tips: [
        'Wash hands frequently to prevent spreading bacteria',
        'Keep your skin clean and dry, especially in skin folds',
        'Change pillowcases regularly to reduce bacteria buildup',
        'Avoid sharing personal items like towels and razors',
        'Shower after sweating or exercising'
      ]
    },
    {
      title: 'Lifestyle Habits',
      icon: '💪',
      tips: [
        'Maintain a balanced diet rich in vitamins and antioxidants',
        'Get 7-9 hours of quality sleep each night',
        'Manage stress through meditation or relaxation techniques',
        'Exercise regularly to improve blood circulation',
        'Avoid smoking and excessive alcohol consumption'
      ]
    },
    {
      title: 'Environmental Care',
      icon: '🌿',
      tips: [
        'Use a humidifier in dry environments to prevent skin dryness',
        'Avoid extremely hot water when bathing or showering',
        'Wear gloves when using harsh chemicals or cleaning products',
        'Choose fragrance-free and hypoallergenic products',
        'Patch test new skincare products before full application'
      ]
    },
    {
      title: 'Medical Awareness',
      icon: '🩺',
      tips: [
        'Perform monthly self-examinations for unusual moles or spots',
        'Schedule annual skin check-ups with a dermatologist',
        'Seek medical attention for persistent or worsening conditions',
        'Keep track of any changes in existing skin conditions',
        'Follow prescribed treatment plans consistently'
      ]
    }
  ];

  return (
    <div className="precautions-page">
      <div className="page-header">
        <h1 className="page-title">
          <span className="title-icon">🛡️</span>
          Skin Care Precautions
        </h1>
        <p className="page-description">
          Essential tips and preventive measures for maintaining healthy skin
        </p>
      </div>

      <div className="precautions-grid">
        {precautionCategories.map((category, index) => (
          <div key={index} className="precaution-card">
            <div className="precaution-header">
              <span className="precaution-icon">{category.icon}</span>
              <h2 className="precaution-title">{category.title}</h2>
            </div>
            <ul className="precaution-list">
              {category.tips.map((tip, idx) => (
                <li key={idx} className="precaution-item">{tip}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="emergency-box">
        <div className="emergency-header">
          <span className="emergency-icon">🚨</span>
          <h2>When to Seek Immediate Medical Attention</h2>
        </div>
        <ul className="emergency-list">
          <li>Sudden appearance of severe rashes or hives</li>
          <li>Rapidly spreading skin infections</li>
          <li>Severe pain, swelling, or bleeding</li>
          <li>Signs of infection: fever, pus, or warm, red skin</li>
          <li>Moles that change shape, color, or size rapidly</li>
          <li>Allergic reactions with breathing difficulties</li>
        </ul>
      </div>

      <div className="tips-box">
        <h2>💡 Quick Tips for Healthy Skin</h2>
        <div className="tips-grid">
          <div className="tip-item">
            <span className="tip-emoji">🥗</span>
            <p>Eat foods rich in vitamins C, E, and omega-3 fatty acids</p>
          </div>
          <div className="tip-item">
            <span className="tip-emoji">💧</span>
            <p>Keep your skin hydrated from inside out</p>
          </div>
          <div className="tip-item">
            <span className="tip-emoji">😴</span>
            <p>Get adequate sleep for skin regeneration</p>
          </div>
          <div className="tip-item">
            <span className="tip-emoji">🚭</span>
            <p>Avoid smoking to prevent premature aging</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PrecautionsPage;
