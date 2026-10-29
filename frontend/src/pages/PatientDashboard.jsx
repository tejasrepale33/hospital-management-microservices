import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { patientService } from '../services/patientService';
import UrgencyBadge from '../components/UrgencyBadge';
import DoctorCard from '../components/DoctorCard';
import SkeletonLoader from '../components/SkeletonLoader';

const PatientDashboard = () => {
  const { user } = useAuth();

  // Triage state
  const [symptoms, setSymptoms] = useState('');
  const [durationDays, setDurationDays] = useState('2');
  const [existingConditions, setExistingConditions] = useState('');
  const [triageResult, setTriageResult] = useState(null);
  const [triaging, setTriaging] = useState(false);
  const [triageError, setTriageError] = useState('');

  // Booking modal / success state
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [bookingDate, setBookingDate] = useState(new Date().toISOString().split('T')[0]);
  const [bookingSuccess, setBookingSuccess] = useState('');
  const [bookingLoading, setBookingLoading] = useState(false);

  // Past appointments
  const [appointments, setAppointments] = useState([]);
  const [loadingAppointments, setLoadingAppointments] = useState(false);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    setLoadingAppointments(true);
    try {
      // Default patient ID 1 for demonstration
      const data = await patientService.getAppointments(1);
      setAppointments(data || []);
    } catch {
      // Fallback
    } finally {
      setLoadingAppointments(false);
    }
  };

  const handleTriageSubmit = async (e) => {
    e.preventDefault();
    if (!symptoms.trim()) return;

    setTriaging(true);
    setTriageError('');
    setTriageResult(null);

    try {
      const response = await patientService.triageSymptoms({
        symptoms,
        age: 38,
        gender: 'MALE',
        durationDays: parseInt(durationDays, 10) || 1,
        existingConditions: existingConditions || 'None reported'
      });
      setTriageResult(response);
    } catch (err) {
      setTriageError(err.response?.data?.error || err.message || 'AI Triage service temporarily unavailable');
    } finally {
      setTriaging(false);
    }
  };

  const handleQuickSymptom = (text) => {
    setSymptoms(text);
  };

  const handleBookSlotClick = (doctor, slot) => {
    setSelectedDoctor(doctor);
    setSelectedSlot(slot);
  };

  const confirmBooking = async () => {
    if (!selectedDoctor) return;
    setBookingLoading(true);
    setBookingSuccess('');

    try {
      await patientService.bookAppointment(1, {
        doctorId: selectedDoctor.id,
        doctorName: selectedDoctor.name,
        department: selectedDoctor.department,
        appointmentDate: bookingDate,
        timeSlot: selectedSlot ? `${selectedSlot.dayOfWeek}: ${selectedSlot.startTime}` : '10:00 AM - 11:00 AM',
        symptoms: symptoms || 'Routine consultation',
        notes: `Triage Referral: ${triageResult ? triageResult.urgencyLevel : 'General'}`
      });

      setBookingSuccess(`Appointment successfully confirmed with ${selectedDoctor.name}!`);
      setSelectedDoctor(null);
      setSelectedSlot(null);
      fetchAppointments();
    } catch (err) {
      alert('Booking failed: ' + (err.response?.data?.error || err.message));
    } finally {
      setBookingLoading(false);
    }
  };

  return (
    <div>
      {/* Welcome Banner */}
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h1 style={{ fontSize: '1.85rem', color: 'var(--primary-dark)', marginBottom: '0.25rem' }}>
              Patient Health Portal
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Hello, <strong>{user?.username}</strong>. Check your symptoms with our AI assistant or view your upcoming consultations.
            </p>
          </div>
          <a href="/book" className="btn btn-secondary">
            📅 Book Specialist Appointment
          </a>
        </div>
      </div>

      {bookingSuccess && (
        <div
          style={{
            padding: '1rem 1.25rem',
            background: 'var(--urgency-low-bg)',
            border: '1px solid #5EEAD4',
            borderRadius: 'var(--radius-md)',
            color: 'var(--urgency-low)',
            fontWeight: '600',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}
        >
          <span>✓ {bookingSuccess}</span>
          <button onClick={() => setBookingSuccess('')} style={{ color: 'inherit', fontWeight: 'bold' }}>✕</button>
        </div>
      )}

      {/* Main Grid: AI Triage Form & Result */}
      <div className="grid-2" style={{ marginBottom: '2.5rem' }}>
        {/* Left Column: Symptom Input Card */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1.25rem' }}>
            <span style={{ fontSize: '1.4rem' }}>🩺</span>
            <div>
              <h2 style={{ fontSize: '1.25rem', color: 'var(--primary-dark)' }}>
                AI Symptom Checker
              </h2>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                Intelligent severity evaluation & department matching
              </p>
            </div>
          </div>

          {/* Quick symptom chip prompts */}
          <div style={{ marginBottom: '1.25rem' }}>
            <div style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
              Test Clinical Scenarios:
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
              <button
                type="button"
                onClick={() => handleQuickSymptom('Severe chest pain radiating to left arm and breathlessness')}
                style={{
                  fontSize: '0.75rem',
                  padding: '0.35rem 0.65rem',
                  borderRadius: 'var(--radius-full)',
                  background: 'var(--urgency-emergency-bg)',
                  color: 'var(--urgency-emergency)',
                  border: '1px solid #FCA5A5',
                  fontWeight: '600'
                }}
              >
                🚨 Cardiac Emergency
              </button>
              <button
                type="button"
                onClick={() => handleQuickSymptom('Red itchy rash on forearms and mild swelling')}
                style={{
                  fontSize: '0.75rem',
                  padding: '0.35rem 0.65rem',
                  borderRadius: 'var(--radius-full)',
                  background: 'var(--urgency-moderate-bg)',
                  color: '#B45309',
                  border: '1px solid #FCD34D',
                  fontWeight: '600'
                }}
              >
                ⏱️ Dermatology
              </button>
              <button
                type="button"
                onClick={() => handleQuickSymptom('Persistent migraine headache and sensitivity to light')}
                style={{
                  fontSize: '0.75rem',
                  padding: '0.35rem 0.65rem',
                  borderRadius: 'var(--radius-full)',
                  background: 'var(--urgency-high-bg)',
                  color: 'var(--urgency-high)',
                  border: '1px solid #FB923C',
                  fontWeight: '600'
                }}
              >
                ⚠️ Neurology
              </button>
              <button
                type="button"
                onClick={() => handleQuickSymptom('Severe knee joint pain and swelling after playing football')}
                style={{
                  fontSize: '0.75rem',
                  padding: '0.35rem 0.65rem',
                  borderRadius: 'var(--radius-full)',
                  background: 'var(--primary-light)',
                  color: 'var(--primary)',
                  border: '1px solid #CBD5E1',
                  fontWeight: '600'
                }}
              >
                🦴 Orthopedics
              </button>
            </div>
          </div>

          {triageError && (
            <div
              style={{
                padding: '0.75rem',
                background: 'var(--urgency-emergency-bg)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--urgency-emergency)',
                fontSize: '0.85rem',
                marginBottom: '1rem'
              }}
            >
              {triageError}
            </div>
          )}

          <form onSubmit={handleTriageSubmit}>
            <div className="form-group">
              <label className="form-label">Describe your symptoms *</label>
              <textarea
                required
                className="form-textarea"
                rows={4}
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                placeholder="e.g. I have had a sharp pain in my chest for the last hour with shortness of breath..."
              />
            </div>

            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Duration (Days)</label>
                <input
                  type="number"
                  min="1"
                  className="form-input"
                  value={durationDays}
                  onChange={(e) => setDurationDays(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Pre-existing Conditions</label>
                <input
                  type="text"
                  className="form-input"
                  value={existingConditions}
                  onChange={(e) => setExistingConditions(e.target.value)}
                  placeholder="e.g. Hypertension, Asthma"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={triaging || !symptoms.trim()}
              className="btn btn-primary"
              style={{ width: '100%', padding: '0.75rem' }}
            >
              {triaging ? 'Analyzing your symptoms...' : '🔍 Analyze My Symptoms'}
            </button>
          </form>
        </div>

        {/* Right Column: AI Triage Results */}
        <div>
          {triaging ? (
            <div className="card" style={{ padding: '2rem' }}>
              <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🤖</div>
                <h3 style={{ color: 'var(--primary-dark)' }}>Analyzing Your Symptoms...</h3>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  Evaluating your condition, estimating urgency, and finding the right specialists for you...
                </p>
              </div>
              <SkeletonLoader type="card" count={2} />
            </div>
          ) : triageResult ? (
            <div
              className="card"
              style={{
                border:
                  triageResult.urgencyLevel === 'EMERGENCY'
                    ? '2px solid #F87171'
                    : '1px solid var(--border-light)',
                boxShadow:
                  triageResult.urgencyLevel === 'EMERGENCY'
                    ? '0 12px 30px -4px rgba(230, 57, 70, 0.2)'
                    : 'var(--shadow-md)'
              }}
            >
              {/* Header Badge & Department */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.75rem' }}>
                <div>
                  <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: '700', textTransform: 'uppercase' }}>
                    Clinical Urgency Level:
                  </span>
                  <div style={{ marginTop: '0.3rem' }}>
                    <UrgencyBadge level={triageResult.urgencyLevel} pulse={true} />
                  </div>
                </div>

                <div style={{ textAlign: 'right' }}>
                  <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: '700', textTransform: 'uppercase' }}>
                    Recommended Department:
                  </span>
                  <div style={{ fontSize: '1.15rem', fontWeight: '800', color: 'var(--primary-dark)', marginTop: '0.1rem' }}>
                    🏥 {triageResult.recommendedDepartment}
                  </div>
                </div>
              </div>

              {/* Clinical Hypothesis */}
              <div
                style={{
                  background: 'var(--bg-subtle)',
                  padding: '1rem',
                  borderRadius: 'var(--radius-md)',
                  marginBottom: '1.25rem',
                  borderLeft: '4px solid var(--primary)'
                }}
              >
                <div style={{ fontSize: '0.8rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.2rem' }}>
                  Diagnostic Hypothesis:
                </div>
                <div style={{ fontWeight: '600', color: 'var(--text-main)', fontSize: '0.95rem' }}>
                  {triageResult.diagnosisHypothesis}
                </div>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>
                  {triageResult.aiAnalysisSummary}
                </p>
              </div>

              {/* Precautions */}
              {triageResult.preliminaryPrecautions && triageResult.preliminaryPrecautions.length > 0 && (
                <div style={{ marginBottom: '1.25rem' }}>
                  <h4 style={{ fontSize: '0.9rem', color: 'var(--primary-dark)', marginBottom: '0.5rem' }}>
                    🛡️ Immediate Precautions:
                  </h4>
                  <ul style={{ paddingLeft: '1.2rem', fontSize: '0.85rem', color: 'var(--text-main)' }}>
                    {triageResult.preliminaryPrecautions.map((item, idx) => (
                      <li key={idx} style={{ marginBottom: '0.25rem' }}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Recommended Diagnostic Tests */}
              {triageResult.recommendedLabTests && triageResult.recommendedLabTests.length > 0 && (
                <div style={{ marginBottom: '1.25rem' }}>
                  <h4 style={{ fontSize: '0.9rem', color: 'var(--primary-dark)', marginBottom: '0.5rem' }}>
                    🧪 Suggested Diagnostic Tests:
                  </h4>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                    {triageResult.recommendedLabTests.map((test, idx) => (
                      <span
                        key={idx}
                        style={{
                          fontSize: '0.78rem',
                          background: 'var(--primary-light)',
                          color: 'var(--primary-dark)',
                          padding: '0.2rem 0.55rem',
                          borderRadius: 'var(--radius-sm)',
                          fontWeight: '600'
                        }}
                      >
                        {test}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Matched Specialists from Doctor Service */}
              <div>
                <h4 style={{ fontSize: '0.9rem', color: 'var(--primary-dark)', marginBottom: '0.75rem' }}>
                  👨‍⚕️ Available {triageResult.recommendedDepartment} Specialists:
                </h4>

                {triageResult.suggestedDoctors && triageResult.suggestedDoctors.length > 0 ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                    {triageResult.suggestedDoctors.map((doc) => (
                      <DoctorCard key={doc.id} doctor={doc} onBookSlot={handleBookSlotClick} />
                    ))}
                  </div>
                ) : (
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    No direct department doctors currently listed. Click below to browse all hospital specialists.
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div
              className="card"
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '3rem 2rem',
                textAlign: 'center',
                color: 'var(--text-muted)'
              }}
            >
              <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🤖</div>
              <h3 style={{ color: 'var(--text-main)', marginBottom: '0.5rem' }}>
                AI Clinical Decision Support
              </h3>
              <p style={{ fontSize: '0.9rem', maxWidth: '380px' }}>
                Describe your symptoms on the left to receive automated urgency triage, specialist recommendations, and immediate medical precautions.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Booking Modal / Dialog */}
      {selectedDoctor && (
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
          <div className="card" style={{ maxWidth: '480px', width: '100%', animation: 'fadeIn 0.2s ease' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <h3 style={{ fontSize: '1.2rem', color: 'var(--primary-dark)' }}>
                Confirm Consultation
              </h3>
              <button
                onClick={() => setSelectedDoctor(null)}
                style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}
              >
                ✕
              </button>
            </div>

            <div style={{ background: 'var(--primary-light)', padding: '1rem', borderRadius: 'var(--radius-md)', marginBottom: '1.25rem' }}>
              <div style={{ fontWeight: '700', color: 'var(--primary-dark)' }}>{selectedDoctor.name}</div>
              <div style={{ fontSize: '0.85rem', color: 'var(--primary)' }}>
                {selectedDoctor.department} • {selectedDoctor.specialization}
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--accent-dark)', fontWeight: '700', marginTop: '0.3rem' }}>
                Consultation Fee: ${selectedDoctor.consultationFee || 120}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Consultation Date</label>
              <input
                type="date"
                className="form-input"
                value={bookingDate}
                onChange={(e) => setBookingDate(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Selected Slot</label>
              <input
                type="text"
                readOnly
                className="form-input"
                value={selectedSlot ? `${selectedSlot.dayOfWeek}: ${selectedSlot.startTime} - ${selectedSlot.endTime}` : 'Morning Slot (09:00 AM - 10:00 AM)'}
              />
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.5rem' }}>
              <button
                type="button"
                onClick={() => setSelectedDoctor(null)}
                className="btn btn-outline"
                style={{ flex: 1 }}
              >
                Cancel
              </button>
              <button
                type="button"
                disabled={bookingLoading}
                onClick={confirmBooking}
                className="btn btn-primary"
                style={{ flex: 1 }}
              >
                {bookingLoading ? 'Confirming...' : 'Confirm Appointment'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Appointment History Section */}
      <div>
        <h2 style={{ fontSize: '1.4rem', color: 'var(--primary-dark)', marginBottom: '1rem' }}>
          My Consultations & Appointments
        </h2>

        {loadingAppointments ? (
          <SkeletonLoader type="card" count={2} />
        ) : appointments.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
            No appointments booked yet. Use the symptom checker above to find a specialist!
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '1rem' }}>
            {appointments.map((appt) => (
              <div key={appt.id} className="card" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <span
                    style={{
                      fontSize: '0.75rem',
                      fontWeight: '700',
                      padding: '0.2rem 0.6rem',
                      borderRadius: 'var(--radius-full)',
                      backgroundColor: appt.status === 'CONFIRMED' ? 'var(--urgency-low-bg)' : 'var(--primary-light)',
                      color: appt.status === 'CONFIRMED' ? 'var(--urgency-low)' : 'var(--primary)'
                    }}
                  >
                    {appt.status || 'SCHEDULED'}
                  </span>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    📅 {appt.appointmentDate || 'Upcoming'}
                  </span>
                </div>

                <div style={{ fontWeight: '700', color: 'var(--text-main)', fontSize: '1.05rem' }}>
                  {appt.doctorName || 'Specialist Consultation'}
                </div>
                <div style={{ fontSize: '0.85rem', color: 'var(--primary)', marginBottom: '0.5rem' }}>
                  {appt.department || 'General Medicine'}
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  <strong>Time:</strong> {appt.timeSlot || '10:00 AM'}
                </div>
                {appt.notes && (
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.4rem', fontStyle: 'italic' }}>
                    "{appt.notes}"
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientDashboard;
