import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  const linkStyle = (path) => ({
    padding: '0.45rem 0.9rem',
    borderRadius: 'var(--radius-md)',
    fontSize: '0.9rem',
    fontWeight: '600',
    color: isActive(path) ? 'var(--primary)' : 'var(--text-muted)',
    backgroundColor: isActive(path) ? 'var(--primary-light)' : 'transparent',
    transition: 'all var(--transition-fast)'
  });

  return (
    <nav
      style={{
        backgroundColor: 'var(--bg-surface)',
        borderBottom: '1px solid var(--border-light)',
        boxShadow: 'var(--shadow-sm)',
        position: 'sticky',
        top: 0,
        zIndex: 50
      }}
    >
      <div
        style={{
          maxWidth: '1280px',
          margin: '0 auto',
          padding: '0.85rem 1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1rem'
        }}
      >
        {/* Brand Logo */}
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, var(--primary), var(--accent))',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '1.25rem',
              fontWeight: '800'
            }}
          >
            ✚
          </div>
          <div>
            <div style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--primary-dark)', letterSpacing: '-0.02em' }}>
              MediPulse
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--accent-dark)', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Smart Healthcare Platform
            </div>
          </div>
        </Link>

        {/* Dynamic Navigation Links based on role */}
        {isAuthenticated && user && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            {user.role === 'PATIENT' && (
              <>
                <Link to="/patient" style={linkStyle('/patient')}>
                  🩺 AI Symptom Triage
                </Link>
                <Link to="/book" style={linkStyle('/book')}>
                  📅 Book Appointment
                </Link>
              </>
            )}

            {user.role === 'DOCTOR' && (
              <Link to="/doctor" style={linkStyle('/doctor')}>
                👨‍⚕️ Doctor Dashboard
              </Link>
            )}

            {user.role === 'ADMIN' && (
              <>
                <Link to="/admin" style={linkStyle('/admin')}>
                  ⚙️ Admin Console
                </Link>
                <Link to="/book" style={linkStyle('/book')}>
                  📅 Public Booking
                </Link>
              </>
            )}
          </div>
        )}

        {/* Auth User Info & Logout / Login */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {isAuthenticated && user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.88rem', fontWeight: '700', color: 'var(--text-main)' }}>
                  {user.username}
                </div>
                <span
                  style={{
                    display: 'inline-block',
                    fontSize: '0.72rem',
                    fontWeight: '700',
                    padding: '0.15rem 0.5rem',
                    borderRadius: 'var(--radius-full)',
                    backgroundColor:
                      user.role === 'ADMIN'
                        ? '#FEECEE'
                        : user.role === 'DOCTOR'
                        ? '#EBF3F8'
                        : '#E6FAF8',
                    color:
                      user.role === 'ADMIN'
                        ? 'var(--urgency-emergency)'
                        : user.role === 'DOCTOR'
                        ? 'var(--primary)'
                        : 'var(--accent-dark)'
                  }}
                >
                  {user.role}
                </span>
              </div>

              <button
                onClick={handleLogout}
                className="btn btn-outline"
                style={{ padding: '0.45rem 0.85rem', fontSize: '0.85rem' }}
              >
                Sign Out
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <Link to="/login" className="btn btn-outline" style={{ padding: '0.5rem 1rem' }}>
                Sign In
              </Link>
              <Link to="/register" className="btn btn-primary" style={{ padding: '0.5rem 1rem' }}>
                Register
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
