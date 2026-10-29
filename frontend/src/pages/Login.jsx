import React, { useState } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const isExpired = new URLSearchParams(location.search).get('expired');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const userData = await login(username, password);
      if (userData.role === 'DOCTOR') navigate('/doctor');
      else if (userData.role === 'ADMIN') navigate('/admin');
      else navigate('/patient');
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickFill = (user, pass) => {
    setUsername(user);
    setPassword(pass);
  };

  return (
    <div style={{ maxWidth: '440px', margin: '3rem auto 0', padding: '0 1rem' }}>
      <div className="card" style={{ border: '1px solid var(--border-light)' }}>
        <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
          <div
            style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, var(--primary), var(--accent))',
              color: 'white',
              fontSize: '1.5rem',
              fontWeight: '800',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '0.75rem'
            }}
          >
            ✚
          </div>
          <h2 style={{ fontSize: '1.6rem', color: 'var(--primary-dark)', marginBottom: '0.25rem' }}>
            Welcome to MediPulse
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Hospital Microservices Clinical Portal
          </p>
        </div>

        {isExpired && (
          <div
            style={{
              padding: '0.75rem 1rem',
              background: '#FFFBEB',
              border: '1px solid #FCD34D',
              borderRadius: 'var(--radius-md)',
              color: '#B45309',
              fontSize: '0.85rem',
              marginBottom: '1.25rem'
            }}
          >
            Your session has expired. Please sign in again.
          </div>
        )}

        {error && (
          <div
            style={{
              padding: '0.75rem 1rem',
              background: 'var(--urgency-emergency-bg)',
              border: '1px solid #FCA5A5',
              borderRadius: 'var(--radius-md)',
              color: 'var(--urgency-emergency)',
              fontSize: '0.85rem',
              marginBottom: '1.25rem'
            }}
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              type="text"
              required
              className="form-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. patient_john"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              required
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '0.5rem', padding: '0.75rem' }}
          >
            {loading ? 'Authenticating...' : 'Sign In'}
          </button>
        </form>

        {/* Quick Demo Fill Buttons */}
        <div style={{ marginTop: '1.75rem', paddingTop: '1.25rem', borderTop: '1px solid var(--border-light)' }}>
          <div style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '0.6rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Quick Demo Accounts (Pre-configured):
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.4rem' }}>
            <button
              type="button"
              onClick={() => handleQuickFill('patient_john', 'patient123')}
              className="btn btn-outline"
              style={{ fontSize: '0.75rem', padding: '0.4rem 0.2rem' }}
            >
              👤 Patient
            </button>
            <button
              type="button"
              onClick={() => handleQuickFill('doctor_smith', 'doctor123')}
              className="btn btn-outline"
              style={{ fontSize: '0.75rem', padding: '0.4rem 0.2rem' }}
            >
              👨‍⚕️ Doctor
            </button>
            <button
              type="button"
              onClick={() => handleQuickFill('admin', 'admin123')}
              className="btn btn-outline"
              style={{ fontSize: '0.75rem', padding: '0.4rem 0.2rem' }}
            >
              ⚙️ Admin
            </button>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.88rem', color: 'var(--text-muted)' }}>
          Don't have an account?{' '}
          <Link to="/register" style={{ fontWeight: '600', color: 'var(--primary)' }}>
            Register here
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
