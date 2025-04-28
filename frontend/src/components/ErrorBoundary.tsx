import React, { Component, ErrorInfo, ReactNode } from 'react';
import { useToast } from '../contexts/ToastContext';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundaryBase extends Component<Props & { showToast: (message: string, type: 'error' | 'success' | 'info') => void }, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error, errorInfo: null };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
    this.setState({
      error,
      errorInfo
    });
    this.props.showToast('An error occurred. Please try refreshing the page.', 'error');
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary" role="alert">
          <h2>Something went wrong</h2>
          <p>We apologize for the inconvenience. Please try refreshing the page.</p>
          <button
            onClick={() => window.location.reload()}
            className="retry-button"
          >
            Refresh Page
          </button>
          {process.env.NODE_ENV === 'development' && (
            <details className="error-details">
              <summary>Error Details</summary>
              <pre>{this.state.error?.toString()}</pre>
              <pre>{this.state.errorInfo?.componentStack}</pre>
            </details>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

export const ErrorBoundary: React.FC<Props> = (props) => {
  const { showToast } = useToast();
  return <ErrorBoundaryBase {...props} showToast={showToast} />;
}; 