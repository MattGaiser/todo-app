import React, { createContext, useContext, useState, useCallback } from 'react';
import { Toast } from '../components/Toast';

interface ToastContextType {
  showToast: (message: string, type: 'error' | 'success' | 'info') => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toast, setToast] = useState<{
    message: string;
    type: 'error' | 'success' | 'info';
  } | null>(null);

  const showToast = useCallback((message: string, type: 'error' | 'success' | 'info') => {
    console.log('Showing toast:', { message, type });
    setToast({ message, type });
  }, []);

  const handleClose = useCallback(() => {
    console.log('Closing toast');
    setToast(null);
  }, []);

  console.log('Current toast state:', toast);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={handleClose}
        />
      )}
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (context === undefined) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}; 