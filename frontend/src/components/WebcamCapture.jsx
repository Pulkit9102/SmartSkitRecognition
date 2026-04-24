import React, { useEffect, useRef, useState, useCallback } from 'react';
import './WebcamCapture.css';

/**
 * WebcamCapture
 * Opens the user's webcam, shows a live preview, and on capture produces a
 * File object that is passed to `onCapture(file)` — same shape as the
 * existing upload pipeline expects.
 *
 * Props:
 *  - onCapture(file: File): called with a JPEG File on capture
 *  - onClose(): called when the user dismisses the capture UI
 */
function WebcamCapture({ onCapture, onClose }) {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const [error, setError] = useState(null);
  const [ready, setReady] = useState(false);

  const stopStream = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function start() {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setError('Webcam is not supported in this browser.');
        return;
      }
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
          audio: false,
        });
        if (cancelled) {
          stream.getTracks().forEach((t) => t.stop());
          return;
        }
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.onloadedmetadata = () => {
            videoRef.current?.play().catch(() => {});
            setReady(true);
          };
        }
      } catch (err) {
        if (err && (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError')) {
          setError('Camera permission denied. Please allow camera access and try again.');
        } else if (err && (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError')) {
          setError('No webcam was found on this device.');
        } else {
          setError(err?.message || 'Could not access the webcam.');
        }
      }
    }

    start();
    return () => {
      cancelled = true;
      stopStream();
    };
  }, [stopStream]);

  const handleCapture = useCallback(() => {
    const video = videoRef.current;
    if (!video || !ready) return;

    const w = video.videoWidth;
    const h = video.videoHeight;
    if (!w || !h) return;

    const canvas = document.createElement('canvas');
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, w, h);

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          setError('Failed to capture image. Please try again.');
          return;
        }
        const file = new File([blob], `capture-${Date.now()}.jpg`, {
          type: 'image/jpeg',
          lastModified: Date.now(),
        });
        stopStream();
        onCapture(file);
      },
      'image/jpeg',
      0.92
    );
  }, [ready, stopStream, onCapture]);

  const handleClose = useCallback(() => {
    stopStream();
    onClose?.();
  }, [stopStream, onClose]);

  return (
    <div className="webcam-modal" role="dialog" aria-modal="true">
      <div className="webcam-card">
        <div className="webcam-header">
          <h3>Take a Photo</h3>
          <button type="button" className="webcam-close" onClick={handleClose} aria-label="Close">
            ×
          </button>
        </div>

        {error ? (
          <div className="webcam-error">
            <p>⚠️ {error}</p>
            <button type="button" className="btn btn-secondary" onClick={handleClose}>
              Close
            </button>
          </div>
        ) : (
          <>
            <div className="webcam-video-wrap">
              <video ref={videoRef} className="webcam-video" playsInline muted />
              {!ready && <div className="webcam-loading">Starting camera…</div>}
            </div>
            <div className="webcam-actions">
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleCapture}
                disabled={!ready}
              >
                📸 Capture
              </button>
              <button type="button" className="btn btn-secondary" onClick={handleClose}>
                Cancel
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default WebcamCapture;
