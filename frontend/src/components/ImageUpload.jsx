import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import WebcamCapture from './WebcamCapture.jsx';
import './ImageUpload.css';

function ImageUpload({ onImageSelect, selectedImage }) {
  const [preview, setPreview] = useState(null);
  const [showCamera, setShowCamera] = useState(false);

  useEffect(() => {
    if (selectedImage) {
      const objectUrl = URL.createObjectURL(selectedImage);
      setPreview(objectUrl);
      return () => URL.revokeObjectURL(objectUrl);
    } else {
      setPreview(null);
    }
  }, [selectedImage]);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      onImageSelect(acceptedFiles[0]);
    }
  }, [onImageSelect]);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp']
    },
    multiple: false,
    noClick: true,
    noKeyboard: true,
  });

  const handleCaptured = useCallback((file) => {
    setShowCamera(false);
    onImageSelect(file);
  }, [onImageSelect]);

  const handleRemove = useCallback(() => {
    onImageSelect(null);
  }, [onImageSelect]);

  return (
    <div className="image-upload">
      {!preview ? (
        <>
          <div
            {...getRootProps()}
            className={`dropzone ${isDragActive ? 'active' : ''}`}
            onClick={open}
            role="button"
            tabIndex={0}
          >
            <input {...getInputProps()} />
            <div className="dropzone-content">
              <div className="upload-icon">📤</div>
              {isDragActive ? (
                <p className="dropzone-text">Drop the image here...</p>
              ) : (
                <>
                  <p className="dropzone-text">
                    Drag & drop an image here, or click to select
                  </p>
                  <p className="dropzone-hint">
                    Supported formats: JPEG, PNG, GIF, BMP
                  </p>
                </>
              )}
            </div>
          </div>

          <div className="upload-actions">
            <button
              type="button"
              className="btn btn-primary upload-action-btn"
              onClick={open}
            >
              📁 Upload Image
            </button>
            <button
              type="button"
              className="btn btn-secondary upload-action-btn"
              onClick={() => setShowCamera(true)}
            >
              📷 Take Photo
            </button>
          </div>
        </>
      ) : (
        <div className="preview-container">
          <div className="preview-label">📸 Selected Image:</div>
          <div className="preview-image-wrap">
            <img src={preview} alt="Preview" className="preview-image" />
            <button
              type="button"
              className="preview-remove"
              onClick={handleRemove}
              aria-label="Remove selected image"
              title="Remove image"
            >
              ×
            </button>
          </div>
          <div className="preview-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleRemove}
            >
              🗑️ Remove Image
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => {
                handleRemove();
                setShowCamera(true);
              }}
            >
              📷 Retake Photo
            </button>
          </div>
        </div>
      )}

      {showCamera && (
        <WebcamCapture
          onCapture={handleCaptured}
          onClose={() => setShowCamera(false)}
        />
      )}
    </div>
  );
}

export default ImageUpload;
