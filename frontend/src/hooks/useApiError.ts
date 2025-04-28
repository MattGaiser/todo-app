import { useState } from 'react';
import { ApiError } from '../api';

export const useApiError = () => {
  const [error, setError] = useState<string | null>(null);

  const handleApiError = (err: unknown, defaultMessage: string) => {
    if (err instanceof ApiError) {
      setError(err.message);
    } else {
      setError(defaultMessage);
    }
    console.error(err);
  };

  const clearError = () => setError(null);

  return {
    error,
    handleApiError,
    clearError
  };
}; 