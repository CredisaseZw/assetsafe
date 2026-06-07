import { Link } from 'react-router-dom';
import { AuthPageShell } from '@/components/auth/AuthPageShell';

export default function ForgotPasswordSentPage() {
  return (
    <AuthPageShell
      title="Check your email"
      subtitle="If an account exists for that address, we sent a password reset link. The link expires in 10 minutes."
    >
      <div className="space-y-4 rounded-lg border border-slate-200 bg-slate-50 px-4 py-4 text-sm text-slate-700">
        <p>
          Open the link in the email to verify it, then choose a new password.
          For security, we do not confirm whether the email is registered.
        </p>
        <p>
          Did not receive it? Check spam or request another link from sign in.
        </p>
      </div>
      <p className="text-center text-sm">
        <Link
          to="/login"
          className="font-semibold text-[#0f7d8e] hover:underline"
        >
          Return to sign in
        </Link>
      </p>
    </AuthPageShell>
  );
}
