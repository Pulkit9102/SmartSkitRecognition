import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="title">
          <span className="icon">🔬</span>
          AI Skin Disease Recognition
        </h1>
        <p className="subtitle">
          Advanced machine learning powered skin disease detection and recommendations
        </p>
      </div>
    </header>
  );
}

export default Header;
