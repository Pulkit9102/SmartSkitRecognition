import React, { useState } from 'react';
import './Navigation.css';

const Navigation = ({ currentPage, onNavigate }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const menuItems = [
    { id: 'home', label: 'Home', icon: '🏠' },
    { id: 'check-disease', label: 'Check Disease', icon: '🔍' },
    { id: 'common-diseases', label: 'Common Diseases', icon: '📋' },
    { id: 'precautions', label: 'Precautions', icon: '🛡️' },
    { id: 'about', label: 'About Us', icon: 'ℹ️' }
  ];

  const handleNavigation = (pageId) => {
    onNavigate(pageId);
    setMobileMenuOpen(false);
  };

  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-brand">
          <span className="brand-icon">🏥</span>
          <span className="brand-text">SkinCare AI</span>
        </div>

        <button 
          className="mobile-menu-toggle"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? '✕' : '☰'}
        </button>

        <ul className={`nav-menu ${mobileMenuOpen ? 'mobile-open' : ''}`}>
          {menuItems.map(item => (
            <li key={item.id} className="nav-item">
              <button
                className={`nav-link ${currentPage === item.id ? 'active' : ''}`}
                onClick={() => handleNavigation(item.id)}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

export default Navigation;
