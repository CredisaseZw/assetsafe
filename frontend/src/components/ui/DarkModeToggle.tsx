import React, { useEffect, useState } from 'react';
import { Moon, Sun } from 'lucide-react';

function readStoredTheme() {
  try {
    const t = localStorage.getItem('theme');
    return t === 'dark';
  } catch {
    return false;
  }
}

export default function DarkModeToggle() {
  const [isDark, setIsDark] = useState<boolean>(() => {
    return (
      readStoredTheme() || document.documentElement.classList.contains('dark')
    );
  });

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
      try {
        localStorage.setItem('theme', 'dark');
      } catch (e) {
        void e;
      }
    } else {
      document.documentElement.classList.remove('dark');
      try {
        localStorage.setItem('theme', 'light');
      } catch (e) {
        void e;
      }
    }
  }, [isDark]);

  const handleClick = () => setIsDark((s) => !s);

  return (
    <div>
      <button
        title={
          isDark
            ? 'Dark (click to switch to light)'
            : 'Light (click to switch to dark)'
        }
        aria-pressed={isDark}
        onClick={handleClick}
        className="inline-flex items-center justify-center rounded-md bg-transparent p-1 text-sm hover:bg-slate-100 dark:hover:bg-slate-800"
      >
        {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        <span className="sr-only">Toggle theme</span>
      </button>
    </div>
  );
}
