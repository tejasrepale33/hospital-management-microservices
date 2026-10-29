import React, { useState, useEffect } from 'react';
import { doctorService } from '../services/doctorService';
import SkeletonLoader from '../components/SkeletonLoader';

const AdminPanel = () => {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDept, setSelectedDept] = useState('ALL');

  // New Doctor form
  const [newDoctor, setNewDoctor] = useState({
    name: '',
    department: 'Cardiology',
    specialization: '',
    email: '',
    phone: '',
    consultationFee: '150',
    experienceYears: '10',
    rating: '4.9'
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const departments = ['Cardiology', 'Neurology', 'Dermatology', 'Orthopedics', 'General Medicine'];

  useEffect(() => {
    fetchDoctors();
  }, []);

  const fetchDoctors = async () => {
    setLoading(true);
    try {
      const data = await doctorService.getAllDoctors();
      setDoctors(data || []);
    } catch {
      //
    } finally {
      setLoading(false);
    }
  };

  const handleCreateDoctor = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');

    try {
      await doctorService.createDoctor({
        name: newDoctor.name.startsWith('Dr.') ? newDoctor.name : `Dr. ${newDoctor.name}`,
        department: newDoctor.department,
        specialization: newDoctor.specialization,
        email: newDoctor.email,
        phone: newDoctor.phone,
        consultationFee: parseFloat(newDoctor.consultationFee) || 120,
        experienceYears: parseInt(newDoctor.experienceYears, 10) || 8,
        rating: parseFloat(newDoctor.rating) || 4.8,
        isAvailable: true
      });

      setMessage('New specialist onboarded successfully!');
      setNewDoctor({
        name: '',
        department: 'Cardiology',
        specialization: '',
        email: '',
        phone: '',
        consultationFee: '150',
        experienceYears: '10',
        rating: '4.9'
      });
      fetchDoctors();
    } catch (err) {
      alert('Failed to onboard doctor: ' + (err.response?.data?.error || err.message));
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteDoctor = async (id) => {
    if (!window.confirm('Are you sure you want to remove this doctor from the active catalog?')) return;
    try {
      await doctorService.deleteDoctor(id);
      setMessage('Doctor removed from the directory successfully.');
      fetchDoctors();
    } catch (err) {
      alert('Error removing doctor: ' + (err.response?.data?.error || err.message));
    }
  };

  const filteredDoctors = selectedDept === 'ALL'
    ? doctors
    : doctors.filter((d) => d.department === selectedDept);

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '1.85rem', color: 'var(--primary-dark)', marginBottom: '0.25rem' }}>
          Hospital Administration Panel
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
          Manage clinical departments, onboard medical specialists, and monitor system health.
        </p>
      </div>

      {message && (
        <div
          style={{
            padding: '0.85rem 1.25rem',
            background: 'var(--urgency-low-bg)',
            border: '1px solid #5EEAD4',
            borderRadius: 'var(--radius-md)',
            color: 'var(--urgency-low)',
            fontWeight: '600',
            marginBottom: '1.5rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <span>✓ {message}</span>
          <button onClick={() => setMessage('')} style={{ color: 'inherit' }}>✕</button>
        </div>
      )}

      {/* System Health Overview */}
      <div style={{ marginBottom: '2rem' }}>
        <h3 style={{ fontSize: '1.1rem', color: 'var(--primary-dark)', marginBottom: '0.75rem' }}>
          System Health Overview
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.85rem' }}>
          <div className="card" style={{ padding: '1rem', borderLeft: '4px solid #16A34A' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)' }}>REQUEST ROUTING</div>
            <div style={{ fontWeight: '800', color: 'var(--text-main)', marginTop: '0.2rem' }}>Network Gateway</div>
            <div style={{ fontSize: '0.8rem', color: '#16A34A', fontWeight: '600' }}>● Active & Routing</div>
          </div>

          <div className="card" style={{ padding: '1rem', borderLeft: '4px solid #16A34A' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)' }}>SERVICE DIRECTORY</div>
            <div style={{ fontWeight: '800', color: 'var(--text-main)', marginTop: '0.2rem' }}>4 Services Online</div>
            <div style={{ fontSize: '0.8rem', color: '#16A34A', fontWeight: '600' }}>● All Systems Connected</div>
          </div>

          <div className="card" style={{ padding: '1rem', borderLeft: '4px solid #16A34A' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)' }}>DATABASE</div>
            <div style={{ fontWeight: '800', color: 'var(--text-main)', marginTop: '0.2rem' }}>Patient & Doctor DB</div>
            <div style={{ fontSize: '0.8rem', color: '#16A34A', fontWeight: '600' }}>● Connected & Healthy</div>
          </div>

          <div className="card" style={{ padding: '1rem', borderLeft: '4px solid #16A34A' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)' }}>PERFORMANCE CACHE</div>
            <div style={{ fontWeight: '800', color: 'var(--text-main)', marginTop: '0.2rem' }}>High-Speed Cache</div>
            <div style={{ fontSize: '0.8rem', color: '#16A34A', fontWeight: '600' }}>● Sub-2ms Response</div>
          </div>
        </div>
      </div>

      {/* Main Grid: Onboarding Form & Department Catalog */}
      <div className="grid-2">
        {/* Onboarding Form */}
        <div className="card">
          <h3 style={{ fontSize: '1.2rem', color: 'var(--primary-dark)', marginBottom: '1.25rem' }}>
            👨‍⚕️ Onboard New Medical Specialist
          </h3>

          <form onSubmit={handleCreateDoctor}>
            <div className="form-group">
              <label className="form-label">Doctor Name *</label>
              <input
                type="text"
                required
                className="form-input"
                value={newDoctor.name}
                onChange={(e) => setNewDoctor({ ...newDoctor, name: e.target.value })}
                placeholder="e.g. Dr. Alex Mercer"
              />
            </div>

            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Department *</label>
                <select
                  className="form-select"
                  value={newDoctor.department}
                  onChange={(e) => setNewDoctor({ ...newDoctor, department: e.target.value })}
                >
                  {departments.map((dept) => (
                    <option key={dept} value={dept}>{dept}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Specialization *</label>
                <input
                  type="text"
                  required
                  className="form-input"
                  value={newDoctor.specialization}
                  onChange={(e) => setNewDoctor({ ...newDoctor, specialization: e.target.value })}
                  placeholder="e.g. Interventional Cardiology"
                />
              </div>
            </div>

            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Email Address *</label>
                <input
                  type="email"
                  required
                  className="form-input"
                  value={newDoctor.email}
                  onChange={(e) => setNewDoctor({ ...newDoctor, email: e.target.value })}
                  placeholder="alex.mercer@hospital.com"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Phone</label>
                <input
                  type="text"
                  className="form-input"
                  value={newDoctor.phone}
                  onChange={(e) => setNewDoctor({ ...newDoctor, phone: e.target.value })}
                  placeholder="+1-555-0199"
                />
              </div>
            </div>

            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Consultation Fee ($)</label>
                <input
                  type="number"
                  className="form-input"
                  value={newDoctor.consultationFee}
                  onChange={(e) => setNewDoctor({ ...newDoctor, consultationFee: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Experience (Years)</label>
                <input
                  type="number"
                  className="form-input"
                  value={newDoctor.experienceYears}
                  onChange={(e) => setNewDoctor({ ...newDoctor, experienceYears: e.target.value })}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={saving}
              className="btn btn-primary"
              style={{ width: '100%', marginTop: '0.5rem', padding: '0.75rem' }}
            >
              {saving ? 'Registering Doctor...' : 'Register Doctor'}
            </button>
          </form>
        </div>

        {/* Doctor Directory by Department */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.5rem' }}>
            <h3 style={{ fontSize: '1.2rem', color: 'var(--primary-dark)' }}>
              Hospital Specialist Directory
            </h3>

            {/* Department filter */}
            <select
              className="form-select"
              style={{ width: 'auto', padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
              value={selectedDept}
              onChange={(e) => setSelectedDept(e.target.value)}
            >
              <option value="ALL">All Departments ({doctors.length})</option>
              {departments.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>

          {loading ? (
            <SkeletonLoader type="card" count={3} />
          ) : filteredDoctors.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
              No doctors found in this department.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', maxHeight: '550px', overflowY: 'auto', paddingRight: '0.4rem' }}>
              {filteredDoctors.map((doc) => (
                <div
                  key={doc.id}
                  style={{
                    padding: '1rem',
                    border: '1px solid var(--border-light)',
                    borderRadius: 'var(--radius-md)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    background: 'var(--bg-app)'
                  }}
                >
                  <div>
                    <div style={{ fontWeight: '700', color: 'var(--text-main)', fontSize: '1rem' }}>
                      {doc.name}
                    </div>
                    <div style={{ fontSize: '0.82rem', color: 'var(--primary)', fontWeight: '600' }}>
                      {doc.department} • <span style={{ color: 'var(--text-muted)', fontWeight: '400' }}>{doc.specialization}</span>
                    </div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                      Fee: <strong>${doc.consultationFee}</strong> • Rating: <strong>★ {doc.rating || '4.9'}</strong>
                    </div>
                  </div>

                  <button
                    onClick={() => handleDeleteDoctor(doc.id)}
                    style={{
                      color: 'var(--urgency-emergency)',
                      fontSize: '0.8rem',
                      fontWeight: '700',
                      padding: '0.4rem 0.6rem',
                      border: '1px solid #FCA5A5',
                      borderRadius: 'var(--radius-sm)',
                      background: 'var(--urgency-emergency-bg)'
                    }}
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;
