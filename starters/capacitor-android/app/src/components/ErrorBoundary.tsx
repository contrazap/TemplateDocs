import { Component, type ReactNode } from 'react';

// Shows the error instead of a blank screen if any screen crashes. Data is saved separately, so Reload is safe.
export class ErrorBoundary extends Component<{ children: ReactNode }, { error: Error | null }> {
  state = { error: null as Error | null };

  static getDerivedStateFromError(error: Error) {
    return { error };
  }

  render() {
    const { error } = this.state;
    if (!error) return this.props.children;
    return (
      <div className="splash" style={{ flexDirection: 'column', gap: 12, padding: 24, textAlign: 'center' }}>
        <div style={{ fontWeight: 650, color: 'var(--ink)' }}>Something went wrong on this screen</div>
        <div className="small" style={{ wordBreak: 'break-word' }}>{error.message}</div>
        <button className="btn" onClick={() => location.reload()}>
          Reload
        </button>
      </div>
    );
  }
}
