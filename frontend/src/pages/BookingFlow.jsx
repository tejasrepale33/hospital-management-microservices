import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { doctorService } from '../services/doctorService';
import { patientService } from '../services/patientService';
import DoctorCard from '../components/DoctorCard';
import SkeletonLoader from '../components/SkeletonLoader';

const BookingFlow = () => {
  const navigate = useNavigate();

  // Step state (1: Department, 2: Doctor, 3: Slot, 4: Confirmed)
  const [step, setStep] = useState(1);
  const [selectedDept, setSelectedDept] = useState('');
  const [doctors, setDoctors] = useState([]);
  const [loadingDoctors, setLoadingDoctors] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [bookingDate, setBookingDate] = useState(new Date().toISOString().split('T')[0]);
  const [patientNotes, setPatientNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [confirmedBooking, setConfirmedBooking] = useState(null);

  const departments = [
    { name: 'Cardiology', icon: '❤️', desc: 'Heart, arrhythmia & cardiovascular health' },
    { name: 'Neurology', icon: '🧠', desc: 'Brain, nervous system & stroke care' },
    { name: 'Dermatology', icon: '🧴', desc: 'Skin, hair, allergies & cosmetic health' },
    { name: 'Orthopedics', icon: '🦴', desc: 'Bones, joints, sports injuries & spine' },
    { name: 'General Medicine', icon: '🩺', desc: 'Primary care, checkups & preventative health' }
  ];

  const handleSelectDept = async (deptName) => {
    setSelectedDept(deptName);
    setStep(2);
    setLoadingDoctors(true);

    try {
      const data = await doctorService.getDoctorsByDepartment(deptName);
      setDoctors(data || []);
    } catch {
      setDoctors([]);
    } finally {
      setLoadingDoctors(false);
    }
  };

  const handleSelectDoctorAndSlot = (doctor, slot) => {
    setSelectedDoctor(doctor);
    setSelectedSlot(slot);
    setStep(3);
  };

  const handleConfirmAppointment = async (e) => {
    e.preventDefault();
    if (!selectedDoctor) return;
    setSubmitting(true);

    try {
      const appt = await patientService.bookAppointment(1, {
        doctorId: selectedDoctor.id,
        doctorName: selectedDoctor.name,
        department: selectedDoctor.department,
        appointmentDate: bookingDate,
        timeSlot: selectedSlot ? `${selectedSlot.dayOfWeek}: ${selectedSlot.startTime} - ${selectedSlot.endTime}` : 'Morning Slot (10:00 AM)',
        symptoms: selectedDept + ' consultation',
        notes: patientNotes || 'Booked via MediPulse Booking Flow'
      });

      // Mark slot booked in doctor-service
      if (selectedSlot && selectedSlot.id) {
        try {
          await doctorService.bookSlot(selectedSlot.id);
        } catch {
          //
        }
      }

      setConfirmedBooking(appt);
      setStep(4);
    } catch (err) {
      alert('Booking failed: ' + (err.response?.data?.error || err.message));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '880px', margin: '1rem auto 0' }}>
      {/* Stepper Progress Bar */}
      <div style={{ marginBottom: '2.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', position: 'relative' }}>
          {['1. Select Department', '2. Choose Specialist', '3. Schedule & Details', '4. Confirmation'].map((label, idx) => {
            const stepNum = idx + 1;
            const isDone = step > stepNum;
            const isCurrent = step === stepNum;

            return (
              <div
                key={label}
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  flex: 1,
                  textAlign: 'center'
                }}
              >
                <div
                  style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: '700',
                    fontSize: '0.9rem',
                    backgroundColor: isDone || isCurrent ? 'var(--primary)' : 'var(--border-light)',
                    color: isDone || isCurrent ? 'white' : 'var(--text-muted)',
                    boxShadow: isCurrent ? '0 0 0 4px var(--primary-light)' : 'none',
                    marginBottom: '0.5rem',
                    transition: 'all var(--transition-fast)'
                  }}
                >
                  {isDone ? '✓' : stepNum}
                </div>
                <div style={{ fontSize: '0.82rem', fontWeight: isCurrent ? '700' : '500', color: isCurrent ? 'var(--primary)' : 'var(--text-muted)' }}>
                  {label}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Step 1: Select Department */}
      {step === 1 && (
        <div className="card">
          <h2 style={{ fontSize: '1.4rem', color: 'var(--primary-dark)', marginBottom: '0.5rem' }}>
            Select Medical Department
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
            Choose the clinical discipline for your upcoming consultation.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '1rem' }}>
            {departments.map((dept) => (
              <div
                key={dept.name}
                onClick={() => handleSelectDept(dept.name)}
                style={{
                  padding: '1.25rem',
                  border: '1px solid var(--border-light)',
                  borderRadius: 'var(--radius-lg)',
                  cursor: 'pointer',
                  transition: 'all var(--transition-fast)',
                  background: 'var(--bg-surface)'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.borderColor = 'var(--primary)';
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.borderColor = 'var(--border-light)';
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>{dept.icon}</div>
                <div style={{ fontWeight: '700', fontSize: '1.1rem', color: 'var(--text-main)', marginBottom: '0.25rem' }}>
                  {dept.name}
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  {dept.desc}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Step 2: Choose Doctor */}
      {step === 2 && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <div>
              <h2 style={{ fontSize: '1.4rem', color: 'var(--primary-dark)' }}>
                {selectedDept} Specialists
              </h2>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                All doctor profiles fetched via Spring Cloud LoadBalancer & Redis Cache.
              </p>
            </div>
            <button onClick={() => setStep(1)} className="btn btn-outline" style={{ fontSize: '0.85rem' }}>
              ← Change Department
            </button>
          </div>

          {loadingDoctors ? (
            <SkeletonLoader type="card" count={3} />
          ) : doctors.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
              No doctors currently listed in {selectedDept}.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {doctors.map((doc) => (
                <div key={doc.id}>
                  <DoctorCard
                    doctor={doc}
                    onBookSlot={(doctor, slot) => handleSelectDoctorAndSlot(doctor, slot)}
                  />
                  <div style={{ marginTop: '0.4rem', textAlign: 'right' }}>
                    <button
                      onClick={() => handleSelectDoctorAndSlot(doc, null)}
                      className="btn btn-primary"
                      style={{ fontSize: '0.85rem', padding: '0.45rem 0.9rem' }}
                    >
                      Choose {doc.name} ➔
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Step 3: Schedule & Notes */}
      {step === 3 && selectedDoctor && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h2 style={{ fontSize: '1.4rem', color: 'var(--primary-dark)' }}>
              Appointment Scheduling
            </h2>
            <button onClick={() => setStep(2)} className="btn btn-outline" style={{ fontSize: '0.85rem' }}>
              ← Change Specialist
            </button>
          </div>

          <div style={{ background: 'var(--primary-light)', padding: '1.25rem', borderRadius: 'var(--radius-md)', marginBottom: '1.5rem' }}>
            <div style={{ fontWeight: '800', fontSize: '1.15rem', color: 'var(--primary-dark)' }}>
              {selectedDoctor.name}
            </div>
            <div style={{ fontSize: '0.9rem', color: 'var(--primary)', marginTop: '0.2rem' }}>
              {selectedDoctor.department} • {selectedDoctor.specialization}
            </div>
            <div style={{ fontSize: '0.9rem', color: 'var(--accent-dark)', fontWeight: '700', marginTop: '0.3rem' }}>
              Consultation Fee: ${selectedDoctor.consultationFee || 100} (Payable at clinic)
            </div>
          </div>

          <form onSubmit={handleConfirmAppointment}>
            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Consultation Date *</label>
                <input
                  type="date"
                  required
                  className="form-input"
                  value={bookingDate}
                  onChange={(e) => setBookingDate(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Preferred Time Slot *</label>
                <input
                  type="text"
                  readOnly
                  className="form-input"
                  value={selectedSlot ? `${selectedSlot.dayOfWeek}: ${selectedSlot.startTime} - ${selectedSlot.endTime}` : 'General Slot (10:00 AM - 11:00 AM)'}
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Reason for Visit / Symptoms</label>
              <textarea
                className="form-textarea"
                rows={3}
                value={patientNotes}
                onChange={(e) => setPatientNotes(e.target.value)}
                placeholder="Briefly describe your symptoms or medical concern for the doctor..."
              />
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="btn btn-primary"
              style={{ width: '100%', padding: '0.85rem', fontSize: '1rem', marginTop: '0.5rem' }}
            >
              {submitting ? 'Confirming Appointment...' : 'Complete & Confirm Appointment'}
            </button>
          </form>
        </div>
      )}

      {/* Step 4: Confirmation */}
      {step === 4 && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
          <div
            style={{
              width: '64px',
              height: '64px',
              borderRadius: '50%',
              background: 'var(--urgency-low-bg)',
              color: 'var(--urgency-low)',
              fontSize: '2rem',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '1rem'
            }}
          >
            ✓
          </div>

          <h2 style={{ fontSize: '1.8rem', color: 'var(--primary-dark)', marginBottom: '0.5rem' }}>
            Appointment Confirmed!
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', maxWidth: '480px', margin: '0 auto 1.5rem' }}>
            Your consultation has been scheduled with <strong>{selectedDoctor?.name}</strong>.
          </p>

          <div
            style={{
              background: 'var(--bg-app)',
              border: '1px solid var(--border-light)',
              borderRadius: 'var(--radius-md)',
              padding: '1.25rem',
              maxWidth: '440px',
              margin: '0 auto 2rem',
              textAlign: 'left'
            }}
          >
            <div style={{ marginBottom: '0.5rem' }}>
              <strong>Appointment ID:</strong> #{confirmedBooking?.id || 'APPT-901'}
            </div>
            <div style={{ marginBottom: '0.5rem' }}>
              <strong>Date:</strong> {bookingDate}
            </div>
            <div style={{ marginBottom: '0.5rem' }}>
              <strong>Time:</strong> {selectedSlot ? `${selectedSlot.dayOfWeek}: ${selectedSlot.startTime}` : '10:00 AM'}
            </div>
            <div>
              <strong>Department:</strong> {selectedDoctor?.department}
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
            <button onClick={() => navigate('/patient')} className="btn btn-primary">
              Go to Patient Portal
            </button>
            <button
              onClick={() => {
                setStep(1);
                setSelectedDoctor(null);
                setSelectedSlot(null);
              }}
              className="btn btn-outline"
            >
              Book Another Appointment
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default BookingFlow;
