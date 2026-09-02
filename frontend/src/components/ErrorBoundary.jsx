import React from 'react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("StatLearn AI Application Error:", error, errorInfo);
    this.setState({ errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-[#FAFAF9] flex items-center justify-center p-6 text-[#1C1917]">
          <div className="max-w-md w-full bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] p-6 shadow-md space-y-4 text-xs">
            <div className="space-y-1">
              <h2 className="text-base font-bold text-[#1C1917]">
                Application Error Encountered
              </h2>
              <p className="text-[#78716C]">
                An unexpected interface error occurred. The application recovered safely.
              </p>
            </div>

            {this.state.error && (
              <div className="bg-[#FEF2F2] border border-[#FCA5A5] p-3 rounded text-[11px] text-[#991B1B] font-mono break-all leading-relaxed">
                {this.state.error.toString()}
              </div>
            )}

            <div className="flex items-center gap-2 pt-2 border-t border-[#E7E5E4]">
              <button
                onClick={() => window.location.reload()}
                className="flex-1 py-2 bg-[#991B1B] hover:bg-[#7F1D1D] text-white font-bold text-xs rounded transition shadow-2xs"
              >
                Reload Page
              </button>
              <a
                href="/"
                className="px-4 py-2 bg-stone-100 hover:bg-stone-200 text-[#1C1917] font-semibold text-xs rounded border border-[#E7E5E4] transition"
              >
                Home
              </a>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
