import React from 'react';
import ImageUpload from '../components/ImageUpload.jsx';
import Results from '../components/Results.jsx';
import './CheckDiseasePage.css';

const CheckDiseasePage = ({ 
  selectedImage, 
  results, 
  loading, 
  error, 
  useSerpApi,
  onImageSelect, 
  onAnalyze, 
  onReset,
  onToggleSerpApi 
}) => {
  return (
    <div className="check-disease-page">
      <div className="page-header">
        <h1 className="page-title">
          <span className="title-icon">🔍</span>
          Skin Disease Detection
        </h1>
        <p className="page-description">
          Upload a clear image of the affected skin area for AI-powered analysis
        </p>
      </div>

      <div className="upload-section">
        <ImageUpload
          onImageSelect={onImageSelect}
          selectedImage={selectedImage}
        />

        {selectedImage && !results && (
          <div className="serp-option">
            <input
              type="checkbox"
              id="serp-toggle"
              checked={useSerpApi}
              onChange={(e) => onToggleSerpApi(e.target.checked)}
            />
            <label htmlFor="serp-toggle">
              Get web recommendations (SerpAPI)
            </label>
          </div>
        )}

        {selectedImage && !results && (
          <div className="button-group">
            <button
              onClick={onAnalyze}
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? 'Analyzing...' : '🔬 Analyze Image'}
            </button>
            <button
              onClick={onReset}
              className="btn btn-secondary"
            >
              ↺ Upload New Image
            </button>
          </div>
        )}
      </div>

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Analyzing your image with AI...</p>
        </div>
      )}

        {error && (
        <div className="error-message">
        <p><strong>⚠️ {error.error}</strong></p>
        <p>{error.message}</p>

        {error.error === "Unsupported file format" && (
          <p>💡 Tip: Use JPG, JPEG, or PNG images only.</p>
        )}

        {error.error === "Not a skin image" && (
          <p>💡 Tip: Upload a clear image of skin area.</p>
        )}
        </div>
    )}

      {results && (
        <>
          <Results results={results} />
          <div className="button-group" style={{ marginTop: '2rem' }}>
            <button onClick={onReset} className="btn btn-primary">
              ↺ Analyze Another Image
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default CheckDiseasePage;
