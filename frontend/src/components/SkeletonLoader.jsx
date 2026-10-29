import React from 'react';

const SkeletonLoader = ({ type = 'card', count = 1 }) => {
  const shimmerStyle = {
    background: 'linear-gradient(90deg, #F1F5F9 25%, #E2E8F0 50%, #F1F5F9 75%)',
    backgroundSize: '200% 100%',
    animation: 'shimmer 1.5s infinite',
    borderRadius: 'var(--radius-md)'
  };

  const renderSkeleton = (key) => {
    if (type === 'card') {
      return (
        <div
          key={key}
          style={{
            background: 'var(--bg-surface)',
            border: '1px solid var(--border-light)',
            borderRadius: 'var(--radius-lg)',
            padding: '1.5rem',
            marginBottom: '1rem',
            boxShadow: 'var(--shadow-sm)'
          }}
        >
          <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ width: '56px', height: '56px', borderRadius: '50%', ...shimmerStyle }} />
            <div style={{ flex: 1 }}>
              <div style={{ width: '60%', height: '18px', marginBottom: '8px', ...shimmerStyle }} />
              <div style={{ width: '40%', height: '14px', ...shimmerStyle }} />
            </div>
          </div>
          <div style={{ width: '100%', height: '14px', marginBottom: '8px', ...shimmerStyle }} />
          <div style={{ width: '80%', height: '14px', marginBottom: '1.25rem', ...shimmerStyle }} />
          <div style={{ width: '35%', height: '32px', ...shimmerStyle }} />
        </div>
      );
    }

    if (type === 'line') {
      return (
        <div
          key={key}
          style={{
            width: '100%',
            height: '20px',
            marginBottom: '10px',
            ...shimmerStyle
          }}
        />
      );
    }

    return null;
  };

  return (
    <div>
      {Array.from({ length: count }).map((_, index) => renderSkeleton(index))}
    </div>
  );
};

export default SkeletonLoader;
