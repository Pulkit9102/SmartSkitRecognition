import React from 'react';
import './HomePage.css';

const HomePage = ({ onNavigate }) => {
  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            <span className="hero-icon">🔬</span>
            AI-Powered Skin Disease Detection
          </h1>
          <p className="hero-subtitle">
            Advanced machine learning technology to help identify skin conditions quickly and accurately
          </p>
          <div className="hero-buttons">
            <button className="btn btn-primary btn-large" onClick={() => onNavigate('check-disease')}>
              <span>🔍</span>
              Check Your Skin
            </button>
            <button className="btn btn-secondary btn-large" onClick={() => onNavigate('common-diseases')}>
              <span>📋</span>
              Learn More
            </button>
          </div>
        </div>
      </section>

      <section className="features-section">
        <h2 className="section-title">Why Choose SkinCare AI?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Fast & Accurate</h3>
            <p>Get instant analysis powered by advanced deep learning models trained on thousands of images</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3>Privacy First</h3>
            <p>Your images are processed securely and never stored on our servers</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🌐</div>
            <h3>Web Research</h3>
            <p>Get comprehensive information and recommendations from trusted medical sources</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📱</div>
            <h3>Easy to Use</h3>
            <p>Simple drag-and-drop interface works on any device, anywhere</p>
          </div>
        </div>
      </section>

      <section className="stats-section">
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-number">95%+</div>
            <div className="stat-label">Accuracy Rate</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">10+</div>
            <div className="stat-label">Skin Conditions</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">24/7</div>
            <div className="stat-label">Availability</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">1000+</div>
            <div className="stat-label">Images Analyzed</div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-content">
          <h2>Ready to Check Your Skin?</h2>
          <p>Upload an image and get instant AI-powered analysis</p>
          <button className="btn btn-primary btn-large" onClick={() => onNavigate('check-disease')}>
            Get Started Now →
          </button>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
