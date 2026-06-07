import { useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@/lib/zodResolver';
import { Eye, EyeOff, Loader2, Lock } from 'lucide-react';
import { toast } from 'sonner';
import { AuthPageShell } from '@/components/auth/AuthPageShell';
import { authApi } from '@/api/authApi';
import { cn } from '@/lib/utils';
import { applyApiValidationErrors } from '@/lib/formErrors';

const passwordSchema = z
  .object({
    new_password: z.string().min(8, 'Password must be at least 8 characters'),
    confirm_password: z.string().min(1, 'Confirm your password'),
  })
  .refine((d) => d.new_password === d.confirm_password, {
    message: 'Passwords must match',
    path: ['confirm_password'],
  });

type PasswordFormValues = z.infer<typeof passwordSchema>;

type Step = 'verifying' | 'invalid' | 'reset' | 'done';

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const uid = searchParams.get('uid') ?? '';
  const token = searchParams.get('token') ?? '';
  const [step, setStep] = useState<Step>('verifying');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<PasswordFormValues>({ resolver: zodResolver(passwordSchema) });

  useEffect(() => {
    if (!uid || !token) {
      setStep('invalid');
      return;
    }

    let cancelled = false;
    async function verify() {
      try {
        await authApi.validatePasswordReset(uid, token);
        if (!cancelled) setStep('reset');
      } catch {
        if (!cancelled) setStep('invalid');
      }
    }
    void verify();
    return () => {
      cancelled = true;
    };
  }, [uid, token]);

  const onSubmit = async (values: PasswordFormValues) => {
    setLoading(true);
    try {
      await authApi.confirmPasswordReset(uid, token, values);
      setStep('done');
      toast.success('Password updated. You can sign in now.');
      setTimeout(() => navigate('/login', { replace: true }), 2000);
    } catch (err: unknown) {
      applyApiValidationErrors(setError, err);
      toast.error('Could not reset password. The link may have expired.');
    } finally {
      setLoading(false);
    }
  };

  if (step === 'verifying') {
    return (
      <AuthPageShell
        title="Verifying link"
        subtitle="Please wait while we confirm your reset link."
      >
        <div className="flex justify-center py-8">
          <Loader2 className="h-8 w-8 animate-spin text-[#0f7d8e]" />
        </div>
      </AuthPageShell>
    );
  }

  if (step === 'invalid') {
    return (
      <AuthPageShell
        title="Invalid or expired link"
        subtitle="Request a new password reset from the sign-in page."
      >
        <p className="text-center text-sm">
          <Link
            to="/forgot-password"
            className="font-semibold text-[#0f7d8e] hover:underline"
          >
            Request new reset link
          </Link>
        </p>
      </AuthPageShell>
    );
  }

  if (step === 'done') {
    return (
      <AuthPageShell
        title="Password updated"
        subtitle="Redirecting you to sign in…"
      >
        <div className="flex justify-center py-4">
          <Loader2 className="h-6 w-6 animate-spin text-[#0f7d8e]" />
        </div>
      </AuthPageShell>
    );
  }

  return (
    <AuthPageShell
      title="Set new password"
      subtitle="Your reset link was verified. Choose a strong password you have not used here before."
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        <div className="space-y-1.5">
          <label className="text-sm font-semibold text-black">
            New password
          </label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              {...register('new_password')}
              type={showPassword ? 'text' : 'password'}
              autoComplete="new-password"
              className={cn(
                'w-full rounded-lg border py-2.5 pl-9 pr-10 text-sm',
                errors.new_password ? 'border-red-500/50' : 'border-slate-300',
              )}
            />
            <button
              type="button"
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400"
              onClick={() => setShowPassword((v) => !v)}
            >
              {showPassword ? (
                <EyeOff className="h-4 w-4" />
              ) : (
                <Eye className="h-4 w-4" />
              )}
            </button>
          </div>
          {errors.new_password ? (
            <p className="text-xs text-red-600">
              {errors.new_password.message}
            </p>
          ) : null}
        </div>

        <div className="space-y-1.5">
          <label className="text-sm font-semibold text-black">
            Confirm password
          </label>
          <input
            {...register('confirm_password')}
            type={showPassword ? 'text' : 'password'}
            autoComplete="new-password"
            className={cn(
              'w-full rounded-lg border px-3 py-2.5 text-sm',
              errors.confirm_password
                ? 'border-red-500/50'
                : 'border-slate-300',
            )}
          />
          {errors.confirm_password ? (
            <p className="text-xs text-red-600">
              {errors.confirm_password.message}
            </p>
          ) : null}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-[#0f7d8e] py-2.5 text-sm font-semibold text-white hover:bg-[#0d6e7e] disabled:opacity-60"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" /> Saving…
            </>
          ) : (
            'Update password'
          )}
        </button>
      </form>
    </AuthPageShell>
  );
}
