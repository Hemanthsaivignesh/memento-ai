import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

function Signup() {
  const { login } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, preferred_language: 'en' }),
      });

      const data = await response.json();

      if (response.ok) {
        login(data.access_token, data.user);
        navigate('/dashboard');
      } else {
        setError(data.detail || 'Signup failed. Please try again.');
      }
    } catch (err) {
      setError('Cannot connect to server. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const inputStyle = {
    width: '100%',
    padding: '0.75rem 1rem',
    background: 'rgba(255,255,255,0.08)',
    border: '1px solid rgba(255,255,255,0.15)',
    borderRadius: '0.625rem',
    color: '#fff',
    fontSize: '0.95rem',
    outline: 'none',
    boxSizing: 'border-box',
    transition: 'border-color 0.2s',
  };

  const labelStyle = {
    display: 'block',
    color: '#cbd5e1',
    fontSize: '0.875rem',
    fontWeight: 500,
    marginBottom: '0.5rem',
  };

  return (
    <BackgroundLayout image={backgroundImages.signup}>
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="max-w-md w-full">
          {/* Logo/Brand */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">Memento AI</h1>
            <p className="text-gray-400">{t('auth.signupTitle')}</p>
          </div>

        {/* Card */}
        <div style={{
          background: 'rgba(255,255,255,0.07)',
          backdropFilter: 'blur(20px)',
          borderRadius: '1.25rem',
          padding: '2rem',
          border: '1px solid rgba(139,92,246,0.2)',
          boxShadow: '0 25px 50px rgba(0,0,0,0.4)',
        }}>
          {error && (
            <div style={{
              marginBottom: '1rem',
              padding: '0.75rem 1rem',
              background: 'rgba(239,68,68,0.15)',
              border: '1px solid rgba(239,68,68,0.4)',
              borderRadius: '0.5rem',
              color: '#fca5a5',
              fontSize: '0.875rem',
            }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '1.1rem' }}>
              <label style={labelStyle}>Full Name</label>
              <input
                id="signup-name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                placeholder="John Doe"
                autoComplete="name"
                style={inputStyle}
                onFocus={(e) => e.target.style.borderColor = 'rgba(139,92,246,0.6)'}
                onBlur={(e) => e.target.style.borderColor = 'rgba(255,255,255,0.15)'}
              />
            </div>

            <div style={{ marginBottom: '1.1rem' }}>
              <label style={labelStyle}>Email</label>
              <input
                id="signup-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
                autoComplete="email"
                style={inputStyle}
                onFocus={(e) => e.target.style.borderColor = 'rgba(139,92,246,0.6)'}
                onBlur={(e) => e.target.style.borderColor = 'rgba(255,255,255,0.15)'}
              />
            </div>

            <div style={{ marginBottom: '1.1rem' }}>
              <label style={labelStyle}>Password</label>
              <input
                id="signup-password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
                placeholder="At least 6 characters"
                autoComplete="new-password"
                style={inputStyle}
                onFocus={(e) => e.target.style.borderColor = 'rgba(139,92,246,0.6)'}
                onBlur={(e) => e.target.style.borderColor = 'rgba(255,255,255,0.15)'}
              />
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Confirm Password</label>
              <input
                id="signup-confirm"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                minLength={6}
                placeholder="Re-enter your password"
                autoComplete="new-password"
                style={inputStyle}
                onFocus={(e) => e.target.style.borderColor = 'rgba(139,92,246,0.6)'}
                onBlur={(e) => e.target.style.borderColor = 'rgba(255,255,255,0.15)'}
              />
            </div>

            <button
              id="signup-submit"
              type="submit"
              disabled={loading}
              style={{
                width: '100%',
                padding: '0.875rem',
                background: loading ? 'rgba(139,92,246,0.4)' : 'linear-gradient(135deg, #7c3aed, #6d28d9)',
                color: '#fff',
                fontWeight: 600,
                fontSize: '1rem',
                borderRadius: '0.625rem',
                border: 'none',
                cursor: loading ? 'not-allowed' : 'pointer',
                transition: 'opacity 0.2s',
                boxShadow: '0 4px 15px rgba(124,58,237,0.4)',
              }}
              onMouseEnter={(e) => { if (!loading) e.target.style.opacity = '0.9'; }}
              onMouseLeave={(e) => { e.target.style.opacity = '1'; }}
            >
              {loading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>

          <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
            <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
              Already have an account?{' '}
              <Link to="/login" style={{ color: '#a78bfa', fontWeight: 500, textDecoration: 'none' }}>
                Sign in
              </Link>
            </p>
          </div>
        </div>

        <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
          <Link to="/" style={{ color: '#64748b', fontSize: '0.875rem', textDecoration: 'none' }}>
            ← Back to home
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Signup;
