interface FieldErrorProps {
  message?: string;
}

export function FieldError({ message }: FieldErrorProps) {
  if (!message) return null;
  return <p className="mt-0.5 text-xs text-red-500">{message}</p>;
}
