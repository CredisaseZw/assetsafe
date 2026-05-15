import { RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Toaster } from 'sonner';
import { router } from '@/routes';
import { hydrate, dehydrate } from '@tanstack/react-query';

type RetryError = {
  response?: {
    status?: number;
  };
  code?: string;
};

// ─── Query client with aggressive caching strategy ───────────────────────────
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Keep data fresh for 5 minutes (reduces background refetches)
      staleTime: 5 * 60 * 1000,
      // Keep inactive data in cache for 30 minutes (larger cache = fewer API calls)
      gcTime: 30 * 60 * 1000,
      // Retry on network errors but not auth errors
      retry: (failureCount, error: unknown) => {
        const retryError = error as RetryError;
        // Never retry auth errors
        if (
          retryError?.response?.status === 401 ||
          retryError?.response?.status === 403
        )
          return false;
        // Retry network errors up to 2 times
        if (retryError?.code === 'ECONNABORTED' || !retryError?.response)
          return failureCount < 2;
        // Retry server errors (5xx) once
        if (retryError?.response?.status && retryError.response.status >= 500)
          return failureCount < 1;
        return false;
      },
      // Avoid aggressive refetching after navigation or refresh.
      refetchOnWindowFocus: false,
      refetchOnReconnect: false,
      refetchOnMount: false,
    },
    mutations: {
      // Retry mutations once on network errors only
      retry: (failureCount, error: unknown) => {
        const retryError = error as RetryError;
        if (retryError?.response?.status && retryError.response.status >= 500)
          return failureCount < 1;
        return false;
      },
    },
  },
});

// Simple React Query persistence using localStorage via dehydrate/hydrate
if (typeof window !== 'undefined') {
  try {
    const cached = window.localStorage.getItem('RQ:cache:v1');
    if (cached) {
      const parsed = JSON.parse(cached);
      hydrate(queryClient, parsed);
    }

    const persist = () => {
      try {
        const data = dehydrate(queryClient);
        window.localStorage.setItem('RQ:cache:v1', JSON.stringify(data));
      } catch {
        // ignore
      }
    };

    window.addEventListener('beforeunload', persist);
    setInterval(persist, 30_000);
    // not removing listeners since app lifecycle equals page lifecycle
  } catch {
    // ignore
  }
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      {/* DevTools: Click the floating button in bottom-right to open query inspector */}
      <ReactQueryDevtools
        initialIsOpen={false}
        buttonPosition="bottom-right"
        position="bottom"
      />
      <Toaster
        position="top-right"
        richColors
        closeButton
        toastOptions={{
          duration: 4000,
          style: { fontFamily: 'Inter, system-ui, sans-serif' },
        }}
      />
    </QueryClientProvider>
  );
}
