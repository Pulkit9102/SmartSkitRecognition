import React, { useState, useCallback } from 'react';
import './App.css';
import Navigation from './components/Navigation';
import HomePage from './pages/HomePage';
import CheckDiseasePage from './pages/CheckDiseasePage';
import CommonDiseasesPage from './pages/CommonDiseasesPage';
import PrecautionsPage from './pages/PrecautionsPage';
import AboutPage from './pages/AboutPage';
import AuthPage from './pages/AuthPage';
import apiService from './services/apiService';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedImage, setSelectedImage] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [useSerpApi, setUseSerpApi] = useState(true);

  const handleNavigate = (pageId) => {
    setCurrentPage(pageId);
    // Reset disease check state when navigating away
    if (pageId !== 'check-disease') {
      handleReset();
    }
  };

  const handleImageSelect = useCallback((file) => {
    setSelectedImage(file);
    setResults(null);
    setError(null);
  }, []);

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await apiService.predictDisease(selectedImage, useSerpApi);
      setResults(data);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setResults(null);
    setError(null);
  };

  const handleToggleSerpApi = (value) => {
    setUseSerpApi(value);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onNavigate={handleNavigate} />;
      case 'check-disease':
        return (
          <CheckDiseasePage
            selectedImage={selectedImage}
            results={results}
            loading={loading}
            error={error}
            useSerpApi={useSerpApi}
            onImageSelect={handleImageSelect}
            onAnalyze={handleAnalyze}
            onReset={handleReset}
            onToggleSerpApi={handleToggleSerpApi}
          />
        );
      case 'common-diseases':
        return <CommonDiseasesPage />;
      case 'precautions':
        return <PrecautionsPage />;
      case 'about':
        return <AboutPage />;
      case 'auth':
        return <AuthPage />;
      default:
        return <HomePage onNavigate={handleNavigate} />;
    }
  };

  return (
    <div className="App">
      <Navigation currentPage={currentPage} onNavigate={handleNavigate} />
      
      <main className="main-content">
        <div className="container">
          {renderPage()}
        </div>
      </main>

      <footer className="footer">
        <div className="footer-content">
          <p>&copy; 2025 SkinCare AI - Powered by Advanced Machine Learning</p>
          <p className="disclaimer">
            <strong>⚕️ Medical Disclaimer:</strong> This AI tool is for educational and informational purposes only. 
            It is not a substitute for professional medical advice, diagnosis, or treatment. 
            Always consult a qualified dermatologist for accurate diagnosis and treatment.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
