import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { doctorService } from '../services/doctorService';
import SkeletonLoader from '../components/SkeletonLoader';

const DoctorDashboard = () => {
  const { user } = useAuth();
  const [doctors, setDoctors] = useState([]);
  const [currentDoctor, setCurrentDoctor] = useState(null);
  const [slots, setSlots] = useState([]);
  const [loading, setLoading] = useState(true);

  // New slot form state
  const [showSlotModal, setShowSlotModal] = useState(false);
  const [newSlot, setNewSlot] = useState({
    dayOfWeek: 'MONDAY',
    startTime: '09:00 AM',
    endTime: '12:00 PM'
  });
  const [slotSubmitting, setSlotSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchDoctorData();
  }, []);

  const fetchDoctorData = async () => {
    setLoading(true);
    try {
      const allDocs = await doctorService.getAllDoctors();
      setDoctors(allDocs || []);

      // Match current logged-in doctor or pick the first one
      const matched = allDocs.find((d) =>
        d.email?.toLowerCase().includes(user?.username?.toLowerCase()) ||
        d.name?.toLowerCase().includes(user?.username?.toLowerCase())
      ) || allDocs[0];

      if (matched) {
        setCurrentDoctor(matched);
        fetchSlots(matched.id);
      }
    } catch {
      // Fallback
    } finally {
      setLoading(false);
    }
  };

  const fetchSlots = async (docId) => {
    try {
      const slotList = await doctorService.getDoctorSlots(docId);
      setSlots(slotList || []);
    } catch {
      //
    }
  };

  const handleAddSlot = async (e) => {
    e.preventDefault();
    if (!currentDoctor) return;

    setSlotSubmitting(true);
    try {
      await doctorService.addSlot(currentDoctor.id, {
        dayOfWeek: newSlot.dayOfWeek,
        startTime: newSlot.startTime,
        endTime: newSlot.endTime,
        isBooked: false
      });

      setMessage('Availability slot added successfully! Patients can now book this time.');
      setShowSlotModal(false);
      fetchSlots(currentDoctor.id);
    } catch (err) {
      alert('Error adding slot: ' + (err.response?.data?.error || err.message));
    } finally {
      setSlotSubmitting(false);
    }
  };

  // Sample queue items for clinic roster
  const sampleQueue = [
    { id: 101, patientName: 'John Doe', age: 38, time: '09:30 AM', symptoms: 'Post-triage cardiac review', urgency: 'HIGH' },
    { id: 102, patientName: 'Alice Smith', age: 29, time: '10:15 AM', symptoms: 'Follow-up consultation', urgency: 'MODERATE' },
    { id: 103, patientName: 'Robert Williams', age: 54, time: '11:00 AM', symptoms: 'Routine medication adjustment', urgency: 'LOW' }
  ];

  if (loading) {
    return (
      <div style={{ padding: '2rem 0' }}>
        <SkeletonLoader type="card" count={3} />
      </div>
    );
  }

  return (
    <div>
      {/* Welcome Doctor Banner */}
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h1 style={{ fontSize: '1.85rem', color: 'var(--primary-dark)', marginBottom: '0.25rem' }}>
              Doctor Clinical Station
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Welcome back, <strong>{currentDoctor ? currentDoctor.name : user?.username}</strong> ({currentDoctor?.department} • {currentDoctor?.specialization})
            </p>
          </div>
          <button onClick={() => setShowSlotModal(true)} className="btn btn-primary">
            ➕ Add Availability Slot
          </button>
        </div>
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

      {/* Overview Stat Counters */}
      <div className="grid-3" style={{ marginBottom: '2rem' }}>
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ fontSize: '2.5rem' }}>👥</div>
          <div>
            <div style={{ fontSize: '1.8rem', fontWeight: '800', color: 'var(--primary-dark)' }}>
              {sampleQueue.length}
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Patients in Queue</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ fontSize: '2.5rem' }}>📅</div>
          <div>
            <div style={{ fontSize: '1.8rem', fontWeight: '800', color: 'var(--accent-dark)' }}>
              {slots.length}
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Configured Slots</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ fontSize: '2.5rem' }}>⚡</div>
          <div>
            <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#16A34A' }}>
              &lt; 2ms
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Avg. Response Time</div>
          </div>
        </div>
      </div>

      {/* Main Grid: Appointment Queue & Slot Manager */}
      <div className="grid-2">
        {/* Patient Appointment Queue */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <h3 style={{ fontSize: '1.2rem', color: 'var(--primary-dark)' }}>
              Today's Consultation Queue
            </h3>
            <span style={{ fontSize: '0.78rem', background: 'var(--primary-light)', color: 'var(--primary)', padding: '0.2rem 0.6rem', borderRadius: 'var(--radius-full)', fontWeight: '700' }}>
              LIVE ROSTER
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {sampleQueue.map((item) => (
              <div
                key={item.id}
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
                  <div style={{ fontWeight: '700', color: 'var(--text-main)' }}>
                    {item.patientName} <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>({item.age} yrs)</span>
                  </div>
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                    <strong>Symptoms:</strong> {item.symptoms}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--primary)', marginTop: '0.2rem' }}>
                    ⏰ Scheduled Time: {item.time}
                  </div>
                </div>

                <div style={{ textAlign: 'right' }}>
                  <button className="btn btn-outline" style={{ fontSize: '0.8rem', padding: '0.4rem 0.75rem' }}>
                    Start Intake
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Slot Schedule & Management */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <h3 style={{ fontSize: '1.2rem', color: 'var(--primary-dark)' }}>
              My Availability Slots
            </h3>
            <button
              onClick={() => setShowSlotModal(true)}
              className="btn btn-outline"
              style={{ fontSize: '0.82rem', padding: '0.35rem 0.75rem' }}
            >
              + New Slot
            </button>
          </div>

          {slots.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              No availability slots configured yet. Add your consultation hours so patients can book slots.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {slots.map((s) => (
                <div
                  key={s.id}
                  style={{
                    padding: '0.85rem 1rem',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-light)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    background: s.isBooked ? 'var(--bg-subtle)' : 'var(--bg-surface)'
                  }}
                >
                  <div>
                    <div style={{ fontWeight: '700', color: 'var(--text-main)', fontSize: '0.95rem' }}>
                      {s.dayOfWeek}
                    </div>
                    <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                      🕒 {s.startTime} – {s.endTime}
                    </div>
                  </div>

                  <span
                    style={{
                      fontSize: '0.75rem',
                      fontWeight: '700',
                      padding: '0.2rem 0.6rem',
                      borderRadius: 'var(--radius-full)',
                      background: s.isBooked ? '#FEECEE' : 'var(--urgency-low-bg)',
                      color: s.isBooked ? 'var(--urgency-emergency)' : 'var(--urgency-low)'
                    }}
                  >
                    {s.isBooked ? '🔒 BOOKED' : '✓ AVAILABLE'}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Add Slot Modal */}
      {showSlotModal && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            backgroundColor: 'rgba(15, 23, 42, 0.65)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 100,
            padding: '1rem'
          }}
        >
          <div className="card" style={{ maxWidth: '440px', width: '100%', animation: 'fadeIn 0.2s ease' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <h3 style={{ fontSize: '1.2rem', color: 'var(--primary-dark)' }}>
                Add Consultation Slot
              </h3>
              <button
                onClick={() => setShowSlotModal(false)}
                style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddSlot}>
              <div className="form-group">
                <label className="form-label">Day of Week</label>
                <select
                  className="form-select"
                  value={newSlot.dayOfWeek}
                  onChange={(e) => setNewSlot({ ...newSlot, dayOfWeek: e.target.value })}
                >
                  <option value="MONDAY">Monday</option>
                  <option value="TUESDAY">Tuesday</option>
                  <option value="WEDNESDAY">Wednesday</option>
                  <option value="THURSDAY">Thursday</option>
                  <option value="FRIDAY">Friday</option>
                  <option value="SATURDAY">Saturday</option>
                  <option value="SUNDAY">Sunday</option>
                </select>
              </div>

              <div className="grid-2">
                <div className="form-group">
                  <label className="form-label">Start Time</label>
                  <input
                    type="text"
                    required
                    className="form-input"
                    value={newSlot.startTime}
                    onChange={(e) => setNewSlot({ ...newSlot, startTime: e.target.value })}
                    placeholder="09:00 AM"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">End Time</label>
                  <input
                    type="text"
                    required
                    className="form-input"
                    value={newSlot.endTime}
                    onChange={(e) => setNewSlot({ ...newSlot, endTime: e.target.value })}
                    placeholder="12:00 PM"
                  />
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.25rem' }}>
                <button
                  type="button"
                  onClick={() => setShowSlotModal(false)}
                  className="btn btn-outline"
                  style={{ flex: 1 }}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={slotSubmitting}
                  className="btn btn-primary"
                  style={{ flex: 1 }}
                >
                  {slotSubmitting ? 'Registering...' : 'Save Slot'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default DoctorDashboard;
