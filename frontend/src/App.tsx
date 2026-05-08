import { RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';
import { router } from '@/routes';

// ─── Query client with smart caching ─────────────────────────────────────────
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Keep data fresh for 2 minutes; background refetch after that
      staleTime: 2 * 60 * 1000,
      // Keep inactive data in cache for 10 minutes (survives tab switches)
      gcTime: 10 * 60 * 1000,
      // Retry once on failure (avoids hammering the server on 401 during refresh)
      retry: (failureCount, error: any) => {
        // Never retry auth errors
        if (error?.response?.status === 401 || error?.response?.status === 403)
          return false;
        return failureCount < 1;
      },
      refetchOnWindowFocus: true, // Refetch when user switches tabs back
      refetchOnReconnect: true, // Refetch when network comes back
    },
    mutations: {
      retry: 0,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
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
