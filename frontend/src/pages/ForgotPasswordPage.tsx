import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@/lib/zodResolver';
import { Loader2, Mail } from 'lucide-react';
import { toast } from 'sonner';
import { AuthPageShell } from '@/components/auth/AuthPageShell';
import { authApi } from '@/api/authApi';
import { cn } from '@/lib/utils';
import { applyApiValidationErrors } from '@/lib/formErrors';

const schema = z.object({
  email: z.string().email('Enter a valid email address'),
});

type FormValues = z.infer<typeof schema>;

export default function ForgotPasswordPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  const onSubmit = async (values: FormValues) => {
    setLoading(true);
    try {
      await authApi.requestPasswordReset(values.email.trim().toLowerCase());
      navigate('/forgot-password/sent', { replace: true });
    } catch (err: unknown) {
      applyApiValidationErrors(setError, err);
      toast.error('Could not process your request. Try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthPageShell
      title="Forgot password"
      subtitle="Enter the email on your account. If it exists, we will send a secure reset link."
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        <div className="space-y-1.5">
          <label className="text-sm font-semibold text-black">Email</label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              {...register('email')}
              type="email"
              autoComplete="email"
              autoFocus
              placeholder="you@company.com"
              className={cn(
                'w-full rounded-lg border py-2.5 pl-9 pr-3 text-sm',
                errors.email
                  ? 'border-red-500/50'
                  : 'border-slate-300 focus:border-[#0f7d8e]',
              )}
            />
          </div>
          {errors.email ? (
            <p className="text-xs text-red-600">{errors.email.message}</p>
          ) : null}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-[#0f7d8e] py-2.5 text-sm font-semibold text-white hover:bg-[#0d6e7e] disabled:opacity-60"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" /> Sending…
            </>
          ) : (
            'Send reset link'
          )}
        </button>

        <p className="text-center text-sm">
          <Link
            to="/login"
            className="font-semibold text-[#0f7d8e] hover:underline"
          >
            Back to sign in
          </Link>
        </p>
      </form>
    </AuthPageShell>
  );
}
