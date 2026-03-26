import React, { useState } from 'react';
import './AuthPage.css';
import apiService from '../services/apiService';

const initialSignInState = {
  email: '',
  password: ''
};

const initialSignUpState = {
  fullName: '',
  email: '',
  password: '',
  confirmPassword: ''
};

const AuthPage = ({ onAuthSuccess }) => {
  const [activeTab, setActiveTab] = useState('signin');
  const [signInForm, setSignInForm] = useState(initialSignInState);
  const [signUpForm, setSignUpForm] = useState(initialSignUpState);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignInChange = (event) => {
    const { name, value } = event.target;
    setSignInForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSignUpChange = (event) => {
    const { name, value } = event.target;
    setSignUpForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSignInSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setMessage('');

    if (!signInForm.email || !signInForm.password) {
      setError('Please enter your email and password.');
      return;
    }

    setLoading(true);

    try {
      const response = await apiService.login({
        email: signInForm.email,
        password: signInForm.password
      });

      if (response?.token) {
        localStorage.setItem('authToken', response.token);
      }

      if (response?.user) {
        localStorage.setItem('authUser', JSON.stringify(response.user));
      }

      setMessage(`Welcome back, ${response?.user?.name || 'User'}! Login successful.`);
      setSignInForm(initialSignInState);

      if (onAuthSuccess) {
        onAuthSuccess(response?.user || null);
      }
    } catch (submitError) {
      setError(submitError.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSignUpSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setMessage('');

    if (!signUpForm.fullName || !signUpForm.email || !signUpForm.password || !signUpForm.confirmPassword) {
      setError('Please fill all sign up fields.');
      return;
    }

    if (signUpForm.password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    if (signUpForm.password !== signUpForm.confirmPassword) {
      setError('Password and confirm password do not match.');
      return;
    }

    setLoading(true);

    try {
      const response = await apiService.signup({
        name: signUpForm.fullName,
        email: signUpForm.email,
        password: signUpForm.password
      });

      if (response?.token) {
        localStorage.setItem('authToken', response.token);
      }

      if (response?.user) {
        localStorage.setItem('authUser', JSON.stringify(response.user));
      }

      setMessage('Account created successfully. You are now logged in.');
      setSignUpForm(initialSignUpState);
      setActiveTab('signin');

      if (onAuthSuccess) {
        onAuthSuccess(response?.user || null);
      }
    } catch (submitError) {
      setError(submitError.message || 'Signup failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <header className="auth-page-header">
        <h1 className="auth-page-title">
          <span className="auth-title-icon">🔐</span>
          Account Access
        </h1>
        <p className="auth-page-description">
          Securely sign in to your SkinCare AI account or create a new profile.
        </p>
      </header>

      <section className="auth-card">
        <h1>Welcome</h1>
        <p className="auth-subtitle">Sign in to continue or create a new account.</p>

        <div className="auth-tabs">
          <button
            type="button"
            className={`auth-tab ${activeTab === 'signin' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('signin');
              setError('');
              setMessage('');
            }}
          >
            Sign In
          </button>
          <button
            type="button"
            className={`auth-tab ${activeTab === 'signup' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('signup');
              setError('');
              setMessage('');
            }}
          >
            Sign Up
          </button>
        </div>

        {activeTab === 'signin' ? (
          <form className="auth-form" onSubmit={handleSignInSubmit}>
            <label htmlFor="signin-email">Email</label>
            <input
              id="signin-email"
              name="email"
              type="email"
              value={signInForm.email}
              onChange={handleSignInChange}
              placeholder="you@example.com"
            />

            <label htmlFor="signin-password">Password</label>
            <input
              id="signin-password"
              name="password"
              type="password"
              value={signInForm.password}
              onChange={handleSignInChange}
              placeholder="Enter your password"
            />

            <button type="submit" className="btn btn-primary auth-submit" disabled={loading}>
              {loading ? 'Signing In...' : 'Sign In'}
            </button>
          </form>
        ) : (
          <form className="auth-form" onSubmit={handleSignUpSubmit}>
            <label htmlFor="signup-name">Full Name</label>
            <input
              id="signup-name"
              name="fullName"
              type="text"
              value={signUpForm.fullName}
              onChange={handleSignUpChange}
              placeholder="Your full name"
            />

            <label htmlFor="signup-email">Email</label>
            <input
              id="signup-email"
              name="email"
              type="email"
              value={signUpForm.email}
              onChange={handleSignUpChange}
              placeholder="you@example.com"
            />

            <label htmlFor="signup-password">Password</label>
            <input
              id="signup-password"
              name="password"
              type="password"
              value={signUpForm.password}
              onChange={handleSignUpChange}
              placeholder="Create a password"
            />

            <label htmlFor="signup-confirm-password">Confirm Password</label>
            <input
              id="signup-confirm-password"
              name="confirmPassword"
              type="password"
              value={signUpForm.confirmPassword}
              onChange={handleSignUpChange}
              placeholder="Re-enter password"
            />

            <button type="submit" className="btn btn-primary auth-submit" disabled={loading}>
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>
        )}

        {error && <p className="auth-error">{error}</p>}
        {message && <p className="auth-message">{message}</p>}

        <p className="auth-note">
          Your password is encrypted before storage and authentication is token-based.
        </p>
      </section>
    </div>
  );
};

export default AuthPage;
