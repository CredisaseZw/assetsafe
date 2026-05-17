import { Link, useRouteError } from 'react-router-dom';

export default function RouteError() {
  const error = useRouteError() as any;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Unexpected Application Error</h1>
      <p className="mt-2 text-sm text-muted">
        {error?.statusText ??
          error?.message ??
          String(error ?? 'An unknown error occurred')}
      </p>

      <details className="mt-4 whitespace-pre-wrap rounded bg-[#f7f7f7] p-3 text-xs text-slate-800">
        {error?.stack ?? JSON.stringify(error, null, 2)}
      </details>

      <div className="mt-4 flex items-center gap-3">
        <Link to="/" className="btn-primary">
          Go to Dashboard
        </Link>
        <button
          type="button"
          onClick={() => window.location.reload()}
          className="inline-flex items-center gap-2 rounded-sm px-3 py-2 text-sm font-semibold border border-[#8f8f8f] bg-white"
        >
          Reload
        </button>
      </div>
    </div>
  );
}
