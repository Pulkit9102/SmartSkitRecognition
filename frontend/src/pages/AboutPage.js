import React from 'react';
import './AboutPage.css';

const AboutPage = () => {
  return (
    <div className="about-page">
      <div className="page-header">
        <h1 className="page-title">
          <span className="title-icon">ℹ️</span>
          About SkinCare AI
        </h1>
        <p className="page-description">
          Advanced AI technology for early skin disease detection
        </p>
      </div>

      <div className="about-content">
        <section className="about-section">
          <div className="section-icon">🎯</div>
          <h2>Our Mission</h2>
          <p>
            At SkinCare AI, our mission is to make skin disease detection accessible to everyone through 
            cutting-edge artificial intelligence technology. We believe early detection can save lives 
            and improve the quality of life for millions of people worldwide.
          </p>
        </section>

        <section className="about-section">
          <div className="section-icon">🔬</div>
          <h2>Our Technology</h2>
          <p>
            Our platform uses advanced deep learning models based on MobileNetV2 architecture, 
            trained on thousands of dermatological images. The AI system can identify various skin 
            conditions with high accuracy, providing instant analysis and recommendations.
          </p>
          <div className="tech-features">
            <div className="tech-item">
              <span className="tech-badge">🤖</span>
              <strong>Deep Learning</strong>
              <p>State-of-the-art neural networks</p>
            </div>
            <div className="tech-item">
              <span className="tech-badge">📊</span>
              <strong>High Accuracy</strong>
              <p>95%+ detection accuracy</p>
            </div>
            <div className="tech-item">
              <span className="tech-badge">⚡</span>
              <strong>Fast Processing</strong>
              <p>Results in seconds</p>
            </div>
            <div className="tech-item">
              <span className="tech-badge">🔒</span>
              <strong>Secure & Private</strong>
              <p>Your data is protected</p>
            </div>
          </div>
        </section>

        <section className="about-section">
          <div className="section-icon">💡</div>
          <h2>How It Works</h2>
          <div className="steps-container">
            <div className="step-card">
              <div className="step-number">1</div>
              <h3>Upload Image</h3>
              <p>Take a clear photo of the affected skin area and upload it to our platform</p>
            </div>
            <div className="step-arrow">→</div>
            <div className="step-card">
              <div className="step-number">2</div>
              <h3>AI Analysis</h3>
              <p>Our deep learning model analyzes the image and identifies potential conditions</p>
            </div>
            <div className="step-arrow">→</div>
            <div className="step-card">
              <div className="step-number">3</div>
              <h3>Get Results</h3>
              <p>Receive detailed results with confidence levels and recommendations</p>
            </div>
          </div>
        </section>

        <section className="about-section">
          <div className="section-icon">👥</div>
          <h2>Our Team</h2>
          <p>
            We are a dedicated team of AI researchers, dermatologists, and software engineers 
            passionate about leveraging technology to improve healthcare accessibility. Our 
            multidisciplinary approach ensures both technical excellence and medical accuracy.
          </p>
        </section>

        <section className="about-section">
          <div className="section-icon">🌍</div>
          <h2>Our Impact</h2>
          <div className="impact-stats">
            <div className="impact-item">
              <div className="impact-number">1000+</div>
              <div className="impact-label">Images Analyzed</div>
            </div>
            <div className="impact-item">
              <div className="impact-number">10+</div>
              <div className="impact-label">Conditions Detected</div>
            </div>
            <div className="impact-item">
              <div className="impact-number">95%</div>
              <div className="impact-label">Accuracy Rate</div>
            </div>
            <div className="impact-item">
              <div className="impact-number">24/7</div>
              <div className="impact-label">Availability</div>
            </div>
          </div>
        </section>

        <section className="about-section disclaimer-section">
          <div className="section-icon">⚠️</div>
          <h2>Important Notice</h2>
          <div className="disclaimer-content">
            <p>
              <strong>This tool is for educational and informational purposes only.</strong> It is not 
              a substitute for professional medical advice, diagnosis, or treatment. Always seek the 
              advice of qualified healthcare providers with any questions regarding medical conditions.
            </p>
            <p>
              Never disregard professional medical advice or delay seeking it because of information 
              provided by this AI tool. If you have a medical emergency, call your doctor or emergency 
              services immediately.
            </p>
          </div>
        </section>

        <section className="about-section contact-section">
          <div className="section-icon">📧</div>
          <h2>Contact Us</h2>
          <p>
            Have questions or feedback? We'd love to hear from you!
          </p>
          <div className="contact-info">
            <div className="contact-item">
              <span className="contact-icon">📧</span>
              <span>Email: support@skincareai.com</span>
            </div>
            <div className="contact-item">
              <span className="contact-icon">🌐</span>
              <span>Website: www.skincareai.com</span>
            </div>
            <div className="contact-item">
              <span className="contact-icon">📱</span>
              <span>Support: Available 24/7</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default AboutPage;
