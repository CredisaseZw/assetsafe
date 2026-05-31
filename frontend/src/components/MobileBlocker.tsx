import React from 'react';

export function MobileBlocker() {
  const [shouldBlock] = React.useState(() => {
    if (typeof window === 'undefined') {
      return false;
    }

    return (
      navigator.userAgent.match(/Mobi|Android|iPhone|iPad|iPod/i) !== null ||
      (navigator.maxTouchPoints > 0 && window.innerWidth < 1024)
    );
  });

  if (!shouldBlock) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/80 p-4">
      <div className="max-w-md rounded bg-white p-6 text-center">
        <h2 className="mb-2 text-xl font-bold">Unsupported Device</h2>
        <p className="mb-4 text-sm text-slate-700">
          AssetSafe is not available on small or mobile devices. Please open
          this application on a desktop or larger tablet.
        </p>
        <div className="text-sm text-slate-500">
          Thank you for understanding.
        </div>
      </div>
    </div>
  );
}
