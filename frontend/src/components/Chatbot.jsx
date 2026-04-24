import React, { useEffect, useRef, useState, useCallback } from 'react';
import apiService from '../services/apiService';
import './Chatbot.css';

const STORAGE_KEY = 'skincare_chatbot_history_v1';
const MAX_HISTORY = 10; // sent to backend

const WELCOME = {
  role: 'assistant',
  content:
    "Hi! I'm your skincare assistant. Ask me about acne, eczema, sunscreen, routines, or any general skin question. I can't replace a dermatologist, but I'll do my best to help.",
};

function Chatbot() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState(() => {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      const parsed = raw ? JSON.parse(raw) : null;
      if (Array.isArray(parsed) && parsed.length > 0) return parsed;
    } catch { /* ignore */ }
    return [WELCOME];
  });
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const listRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    } catch { /* ignore quota */ }
  }, [messages]);

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages, loading, open]);

  useEffect(() => {
    if (open) {
      // Focus the input shortly after opening
      const t = setTimeout(() => inputRef.current?.focus(), 50);
      return () => clearTimeout(t);
    }
  }, [open]);

  const sendMessage = useCallback(async () => {
    const text = input.trim();
    if (!text || loading) return;
    setError(null);

    const newUserMsg = { role: 'user', content: text };
    const next = [...messages, newUserMsg];
    setMessages(next);
    setInput('');
    setLoading(true);

    // History excludes the just-added user message; backend appends it itself.
    // We also drop the welcome bubble from the wire history.
    const wireHistory = next
      .slice(0, -1)
      .filter((m) => m !== WELCOME)
      .slice(-MAX_HISTORY);

    try {
      const { reply } = await apiService.chat(text, wireHistory);
      setMessages((prev) => [...prev, { role: 'assistant', content: reply }]);
    } catch (err) {
      setError(err?.message || 'Something went wrong. Please try again.');
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Something went wrong. Please try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  }, [input, loading, messages]);

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([WELCOME]);
    setError(null);
    try { sessionStorage.removeItem(STORAGE_KEY); } catch { /* ignore */ }
  };

  return (
    <>
      <button
        type="button"
        className={`chatbot-fab ${open ? 'hidden' : ''}`}
        onClick={() => setOpen(true)}
        aria-label="Open skincare chatbot"
        title="Skincare Assistant"
      >
        💬
      </button>

      {open && (
        <div className="chatbot-window" role="dialog" aria-label="Skincare chatbot">
          <div className="chatbot-header">
            <div className="chatbot-title">
              <span className="chatbot-avatar" aria-hidden="true">🩺</span>
              <div>
                <div className="chatbot-name">Skincare Assistant</div>
                <div className="chatbot-sub">AI · for general guidance only</div>
              </div>
            </div>
            <div className="chatbot-header-actions">
              <button
                type="button"
                className="chatbot-icon-btn"
                onClick={clearChat}
                title="Clear conversation"
                aria-label="Clear conversation"
              >
                ♻️
              </button>
              <button
                type="button"
                className="chatbot-icon-btn"
                onClick={() => setOpen(false)}
                title="Close"
                aria-label="Close chatbot"
              >
                ✕
              </button>
            </div>
          </div>

          <div className="chatbot-messages" ref={listRef}>
            {messages.map((m, i) => (
              <div key={i} className={`chatbot-msg ${m.role}`}>
                <div className="chatbot-bubble">{m.content}</div>
              </div>
            ))}
            {loading && (
              <div className="chatbot-msg assistant">
                <div className="chatbot-bubble typing" aria-label="Assistant is typing">
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}
          </div>

          {error && <div className="chatbot-error">{error}</div>}

          <div className="chatbot-input-row">
            <textarea
              ref={inputRef}
              className="chatbot-input"
              placeholder="Ask a skincare question…"
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKeyDown}
              disabled={loading}
              maxLength={2000}
            />
            <button
              type="button"
              className="chatbot-send"
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              aria-label="Send message"
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default Chatbot;
