import { useState } from 'react';

export function useSessionWatcher() {
  const [secondsLeft, setSecondsLeft] = useState<number | null>(null);

  return { secondsLeft };
}
