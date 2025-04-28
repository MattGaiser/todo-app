import React, { useEffect } from 'react';

interface ToastProps {
  message: string;
  type: 'error' | 'success' | 'info';
  onClose: () => void;
  duration?: number;
}

export const Toast: React.FC<ToastProps> = ({ 
  message, 
  type, 
  onClose, 
  duration = 5000 
}) => {
  console.log('Toast component rendered:', { message, type, duration });

  useEffect(() => {
    console.log('Setting up toast timer');
    const timer = setTimeout(() => {
      console.log('Toast timer expired');
      onClose();
    }, duration);

    return () => {
      console.log('Cleaning up toast timer');
      clearTimeout(timer);
    };
  }, [duration, onClose]);

  const getBackgroundColor = () => {
    switch (type) {
      case 'error':
        return '#f44336';
      case 'success':
        return '#4caf50';
      case 'info':
        return '#2196f3';
      default:
        return '#2196f3';
    }
  };

  return (
    <div 
      className={`toast ${type}`}
      style={{
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 25px',
        backgroundColor: getBackgroundColor(),
        color: 'white',
        borderRadius: '4px',
        boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
        zIndex: 1000,
        animation: 'slideIn 0.3s ease-out'
      }}
      role="alert"
    >
      {message}
      <button 
        onClick={onClose}
        style={{
          background: 'none',
          border: 'none',
          color: 'white',
          marginLeft: '10px',
          cursor: 'pointer',
          fontSize: '16px'
        }}
        aria-label="Close notification"
      >
        ×
      </button>
    </div>
  );
}; 