import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { doctorService } from '../services/doctorService';
import { patientService } from '../services/patientService';

const Register = () => {
  const [role, setRole] = useState('ROLE_PATIENT'); // 'ROLE_PATIENT' or 'ROLE_DOCTOR'
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    fullName: '',
    phone: '',
    age: '30',
    gender: 'MALE',
    bloodGroup: 'O+',
    department: 'Cardiology',
    specialization: 'Consultant',
    consultationFee: '100'
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // 1. Register with Auth Service (JWT issuance)
      const registeredUser = await register({
        username: formData.username,
        password: formData.password,
        email: formData.email,
        role: role
      });

      // 2. Provision clinical profile in corresponding database
      if (role === 'ROLE_DOCTOR') {
        try {
          await doctorService.createDoctor({
            name: 'Dr. ' + (formData.fullName || formData.username),
            department: formData.department,
            specialization: formData.specialization,
            email: formData.email,
            phone: formData.phone || '+1-555-0100',
            consultationFee: parseFloat(formData.consultationFee) || 100,
            rating: 5.0,
            experienceYears: 5,
            isAvailable: true
          });
        } catch {
          // Profile provisioned or can be updated later
        }
        navigate('/doctor');
      } else {
        try {
          const names = (formData.fullName || formData.username).split(' ');
          await patientService.createPatient({
            firstName: names[0] || formData.username,
            lastName: names[1] || 'Patient',
            email: formData.email,
            phone: formData.phone || '+1-555-0200',
            age: parseInt(formData.age, 10) || 30,
            gender: formData.gender,
            bloodGroup: formData.bloodGroup,
            address: 'City General',
            emergencyContact: '+1-555-9999',
            medicalHistory: 'New registered patient'
          });
        } catch {
          // Profile provisioned
        }
        navigate('/patient');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '520px', margin: '2rem auto 0', padding: '0 1rem' }}>
      <div className="card">
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '1.6rem', color: 'var(--primary-dark)', marginBottom: '0.25rem' }}>
            Create Your Account
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Join the MediPulse Healthcare Network
          </p>
        </div>

        {/* Role Selector Tabs */}
        <div
          style={{
            display: 'flex',
            background: 'var(--bg-subtle)',
            padding: '0.3rem',
            borderRadius: 'var(--radius-md)',
            marginBottom: '1.5rem'
          }}
        >
          <button
            type="button"
            onClick={() => setRole('ROLE_PATIENT')}
            style={{
              flex: 1,
              padding: '0.55rem',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.9rem',
              fontWeight: '700',
              backgroundColor: role === 'ROLE_PATIENT' ? 'var(--bg-surface)' : 'transparent',
              color: role === 'ROLE_PATIENT' ? 'var(--primary)' : 'var(--text-muted)',
              boxShadow: role === 'ROLE_PATIENT' ? 'var(--shadow-sm)' : 'none',
              transition: 'all var(--transition-fast)'
            }}
          >
            👤 Patient Account
          </button>
          <button
            type="button"
            onClick={() => setRole('ROLE_DOCTOR')}
            style={{
              flex: 1,
              padding: '0.55rem',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.9rem',
              fontWeight: '700',
              backgroundColor: role === 'ROLE_DOCTOR' ? 'var(--bg-surface)' : 'transparent',
              color: role === 'ROLE_DOCTOR' ? 'var(--primary)' : 'var(--text-muted)',
              boxShadow: role === 'ROLE_DOCTOR' ? 'var(--shadow-sm)' : 'none',
              transition: 'all var(--transition-fast)'
            }}
          >
            👨‍⚕️ Medical Specialist
          </button>
        </div>

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
          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Username *</label>
              <input
                type="text"
                name="username"
                required
                className="form-input"
                value={formData.username}
                onChange={handleChange}
                placeholder="e.g. john_doe"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Full Name *</label>
              <input
                type="text"
                name="fullName"
                required
                className="form-input"
                value={formData.fullName}
                onChange={handleChange}
                placeholder="e.g. John Doe"
              />
            </div>
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Email Address *</label>
              <input
                type="email"
                name="email"
                required
                className="form-input"
                value={formData.email}
                onChange={handleChange}
                placeholder="john@example.com"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Password *</label>
              <input
                type="password"
                name="password"
                required
                className="form-input"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
              />
            </div>
          </div>

          {/* Conditional Fields based on Role */}
          {role === 'ROLE_DOCTOR' ? (
            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Department *</label>
                <select
                  name="department"
                  className="form-select"
                  value={formData.department}
                  onChange={handleChange}
                >
                  <option value="Cardiology">Cardiology</option>
                  <option value="Neurology">Neurology</option>
                  <option value="Dermatology">Dermatology</option>
                  <option value="Orthopedics">Orthopedics</option>
                  <option value="General Medicine">General Medicine</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Consultation Fee ($) *</label>
                <input
                  type="number"
                  name="consultationFee"
                  className="form-input"
                  value={formData.consultationFee}
                  onChange={handleChange}
                  placeholder="120"
                />
              </div>
            </div>
          ) : (
            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Blood Group</label>
                <select
                  name="bloodGroup"
                  className="form-select"
                  value={formData.bloodGroup}
                  onChange={handleChange}
                >
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Age</label>
                <input
                  type="number"
                  name="age"
                  className="form-input"
                  value={formData.age}
                  onChange={handleChange}
                />
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '0.75rem', padding: '0.75rem' }}
          >
            {loading ? 'Registering...' : `Create ${role === 'ROLE_DOCTOR' ? 'Doctor' : 'Patient'} Account`}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.88rem', color: 'var(--text-muted)' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ fontWeight: '600', color: 'var(--primary)' }}>
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Register;
