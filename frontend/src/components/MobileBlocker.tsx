import React from 'react';

export function MobileBlocker() {
  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/80 p-4 sm:hidden">
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
