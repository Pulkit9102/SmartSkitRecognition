import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import './ImageUpload.css';

function ImageUpload({ onImageSelect, selectedImage }) {
  const [preview, setPreview] = useState(null);

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

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp']
    },
    multiple: false
  });

  return (
    <div className="image-upload">
      {!preview ? (
        <div 
          {...getRootProps()} 
          className={`dropzone ${isDragActive ? 'active' : ''}`}
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
      ) : (
        <div className="preview-container">
          <div className="preview-label">📸 Selected Image:</div>
          <img src={preview} alt="Preview" className="preview-image" />
        </div>
      )}
    </div>
  );
}

export default ImageUpload;
