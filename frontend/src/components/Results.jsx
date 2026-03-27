import React from 'react';
import './Results.css';

function Results({ results }) {
  const { prediction, confidence, all_predictions, recommendations, similar_images } = results;

  const formatConfidence = (value) => {
    return (value * 100).toFixed(1);
  };

  const getConfidenceClass = (value) => {
    if (value >= 0.8) return 'high';
    if (value >= 0.5) return 'medium';
    return 'low';
  };

  return (
    <div className="results">
      <h2 className="results-title">Analysis Results</h2>

      {/* Main Prediction */}
      <div className="main-prediction">
        <div className="prediction-header">
          <h3>Predicted Disease</h3>
          <div className={`confidence-badge ${getConfidenceClass(confidence)}`}>
            {formatConfidence(confidence)}% confidence
          </div>
        </div>
        <div className="disease-name">{prediction}</div>
      </div>

      {/* All Predictions */}
      {all_predictions && all_predictions.length > 0 && (
        <div className="all-predictions">
          <h3>Top Predictions</h3>
          <div className="predictions-list">
            {all_predictions.map((pred, index) => (
              <div key={index} className="prediction-item">
                <div className="prediction-info">
                  <span className="rank">#{index + 1}</span>
                  <span className="disease">{pred.disease}</span>
                </div>
                <div className="prediction-bar-container">
                  <div 
                    className="prediction-bar"
                    style={{ width: `${pred.confidence * 100}%` }}
                  />
                  <span className="prediction-percentage">
                    {formatConfidence(pred.confidence)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.recommendations && recommendations.recommendations.length > 0 && (
        <div className="recommendations">
          <h3>🔍 Web Recommendations</h3>
          <p className="search-query">Search: "{recommendations.search_query}"</p>
          <div className="recommendations-list">
            {recommendations.recommendations.map((rec, index) => (
              <div key={index} className="recommendation-item">
                <h4>
                  <a href={rec.link} target="_blank" rel="noopener noreferrer">
                    {rec.title}
                  </a>
                </h4>
                <p>{rec.snippet}</p>
                <a 
                  href={rec.link} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="read-more"
                >
                  Read more →
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Similar Images */}
      {similar_images && similar_images.images && similar_images.images.length > 0 && (
        <div className="similar-images">
          <h3>🖼️ Similar Reference Images</h3>
          <div className="images-grid">
            {similar_images.images.map((img, index) => (
              <div key={index} className="image-item">
                <a href={img.link} target="_blank" rel="noopener noreferrer">
                  <img src={img.thumbnail} alt={`Reference ${index + 1}`} />
                  <div className="image-source">{img.source}</div>
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Medical Disclaimer */}
      <div className="medical-disclaimer">
        <strong>⚠️ Important Medical Disclaimer:</strong>
        <p>
          This is an AI-based educational tool and should not replace professional medical advice.
          Please consult a qualified dermatologist for accurate diagnosis and treatment.
          The predictions and recommendations provided are for informational purposes only.
        </p>
      </div>
    </div>
  );
}

export default Results;
