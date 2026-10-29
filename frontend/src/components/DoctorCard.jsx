import React, { useState } from 'react';

const DoctorCard = ({ doctor, onBookSlot }) => {
  const [expanded, setExpanded] = useState(false);

  const initials = doctor.name
    ? doctor.name
        .replace('Dr. ', '')
        .split(' ')
        .map((n) => n[0])
        .join('')
        .slice(0, 2)
    : 'DR';

  const availableSlots = doctor.availabilitySlots
    ? doctor.availabilitySlots.filter((s) => !s.isBooked)
    : [];

  return (
    <div
      className="card"
      style={{
        padding: '1.5rem',
        border: '1px solid var(--border-light)',
        transition: 'all var(--transition-normal)'
      }}
    >
      <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
        {/* Avatar badge */}
        <div
          style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, var(--primary), var(--accent))',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: '700',
            fontSize: '1.2rem',
            boxShadow: 'var(--shadow-sm)',
            flexShrink: 0
          }}
        >
          {initials}
        </div>

        {/* Doctor Info */}
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: 'var(--text-main)', marginBottom: '0.2rem' }}>
                {doctor.name}
              </h3>
              <div style={{ color: 'var(--primary)', fontWeight: '600', fontSize: '0.9rem' }}>
                {doctor.department} • <span style={{ color: 'var(--text-muted)', fontWeight: '400' }}>{doctor.specialization}</span>
              </div>
            </div>

            {/* Rating pill */}
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.3rem',
                background: '#FEF9EB',
                color: '#B45309',
                padding: '0.25rem 0.65rem',
                borderRadius: 'var(--radius-full)',
                fontWeight: '700',
                fontSize: '0.85rem'
              }}
            >
              ★ {doctor.rating ? doctor.rating.toFixed(1) : '4.8'}
            </div>
          </div>

          <div
            style={{
              display: 'flex',
              gap: '1.5rem',
              marginTop: '0.9rem',
              fontSize: '0.85rem',
              color: 'var(--text-muted)'
            }}
          >
            <div>
              <span style={{ fontWeight: '600', color: 'var(--text-main)' }}>Experience: </span>
              {doctor.experienceYears || 10}+ Years
            </div>
            <div>
              <span style={{ fontWeight: '600', color: 'var(--text-main)' }}>Fee: </span>
              <span style={{ color: 'var(--accent-dark)', fontWeight: '700' }}>${doctor.consultationFee || 100}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Accordion toggle for available slots */}
      <div style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid var(--border-light)' }}>
        <button
          onClick={() => setExpanded(!expanded)}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            width: '100%',
            fontSize: '0.88rem',
            fontWeight: '600',
            color: 'var(--primary)',
            padding: '0.2rem 0'
          }}
        >
          <span>
            {availableSlots.length > 0
              ? `📅 ${availableSlots.length} Available Appointment Slots`
              : '📅 Check Availability & Slots'}
          </span>
          <span style={{ transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }}>
            ▼
          </span>
        </button>

        {/* Smooth Accordion Body */}
        {expanded && (
          <div style={{ marginTop: '0.9rem', animation: 'fadeIn 0.2s ease' }}>
            {availableSlots.length === 0 ? (
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                No active slots listed right now. You can request a custom appointment slot.
              </p>
            ) : (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {availableSlots.map((slot) => (
                  <button
                    key={slot.id}
                    onClick={() => onBookSlot && onBookSlot(doctor, slot)}
                    style={{
                      padding: '0.45rem 0.8rem',
                      borderRadius: 'var(--radius-md)',
                      background: 'var(--primary-light)',
                      border: '1px solid #CBD5E1',
                      color: 'var(--primary-dark)',
                      fontSize: '0.82rem',
                      fontWeight: '600',
                      transition: 'all var(--transition-fast)'
                    }}
                    onMouseOver={(e) => {
                      e.currentTarget.style.background = 'var(--primary)';
                      e.currentTarget.style.color = 'white';
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.background = 'var(--primary-light)';
                      e.currentTarget.style.color = 'var(--primary-dark)';
                    }}
                  >
                    {slot.dayOfWeek}: {slot.startTime} – {slot.endTime}
                  </button>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default DoctorCard;
