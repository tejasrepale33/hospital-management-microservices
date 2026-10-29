import React from 'react';

const UrgencyBadge = ({ level, pulse = true }) => {
  const normLevel = (level || 'LOW').toUpperCase();

  const styles = {
    EMERGENCY: {
      bg: 'var(--urgency-emergency-bg)',
      color: 'var(--urgency-emergency)',
      border: '1px solid #F87171',
      icon: '🚨',
      label: 'EMERGENCY'
    },
    HIGH: {
      bg: 'var(--urgency-high-bg)',
      color: 'var(--urgency-high)',
      border: '1px solid #FB923C',
      icon: '⚠️',
      label: 'HIGH PRIORITY'
    },
    MODERATE: {
      bg: 'var(--urgency-moderate-bg)',
      color: '#B45309',
      border: '1px solid #FCD34D',
      icon: '⏱️',
      label: 'MODERATE'
    },
    LOW: {
      bg: 'var(--urgency-low-bg)',
      color: 'var(--urgency-low)',
      border: '1px solid #5EEAD4',
      icon: '✓',
      label: 'LOW / ROUTINE'
    }
  };

  const config = styles[normLevel] || styles.LOW;
  const isEmergency = normLevel === 'EMERGENCY' && pulse;

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '0.4rem',
        padding: '0.35rem 0.85rem',
        borderRadius: 'var(--radius-full)',
        fontSize: '0.82rem',
        fontWeight: '700',
        letterSpacing: '0.04em',
        backgroundColor: config.bg,
        color: config.color,
        border: config.border,
        animation: isEmergency ? 'pulseEmergency 1.8s infinite' : 'none',
        transition: 'all var(--transition-fast)'
      }}
    >
      <span>{config.icon}</span>
      <span>{config.label}</span>
    </span>
  );
};

export default UrgencyBadge;
