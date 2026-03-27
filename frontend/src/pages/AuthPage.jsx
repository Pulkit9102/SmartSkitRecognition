import React, { useState } from 'react';
import './AuthPage.css';

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

const AuthPage = () => {
  const [activeTab, setActiveTab] = useState('signin');
  const [signInForm, setSignInForm] = useState(initialSignInState);
  const [signUpForm, setSignUpForm] = useState(initialSignUpState);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSignInChange = (event) => {
    const { name, value } = event.target;
    setSignInForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSignUpChange = (event) => {
    const { name, value } = event.target;
    setSignUpForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSignInSubmit = (event) => {
    event.preventDefault();
    setError('');
    setMessage('');

    if (!signInForm.email || !signInForm.password) {
      setError('Please enter your email and password.');
      return;
    }

    setMessage('Sign in form submitted. Connect this to your backend auth API.');
  };

  const handleSignUpSubmit = (event) => {
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

    setMessage('Sign up form submitted. Connect this to your backend auth API.');
  };

  return (
    <div className="auth-page">
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

            <button type="submit" className="btn btn-primary auth-submit">
              Sign In
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

            <button type="submit" className="btn btn-primary auth-submit">
              Create Account
            </button>
          </form>
        )}

        {error && <p className="auth-error">{error}</p>}
        {message && <p className="auth-message">{message}</p>}
      </section>
    </div>
  );
};

export default AuthPage;
