import { toNestErrors } from '@hookform/resolvers';
import type {
  FieldError,
  FieldErrors,
  FieldValues,
  Resolver,
} from 'react-hook-form';
import type { z } from 'zod';

/**
 * Zod v4-compatible resolver for react-hook-form.
 * @hookform/resolvers@3.x only reads ZodError.errors (v3); Zod 4 uses .issues.
 */
function zodIssuesToFieldErrors(
  issues: z.core.$ZodIssue[],
  validateAllFieldCriteria: boolean,
): FieldErrors {
  const errors: Record<string, FieldError> = {};

  for (const issue of issues) {
    const path = issue.path.map(String).join('.');
    if (!path) continue;

    const existing = errors[path];
    if (validateAllFieldCriteria && existing) {
      const types = existing.types ?? {};
      types[issue.code] = issue.message;
      errors[path] = { ...existing, types };
    } else if (!existing) {
      errors[path] = { message: issue.message, type: issue.code };
    }
  }

  return errors;
}

export function zodResolver<T extends z.ZodTypeAny>(
  schema: T,
): Resolver<z.infer<T>> {
  return async (values, _context, options) => {
    const result = schema.safeParse(values);

    if (result.success) {
      return {
        values: result.data,
        errors: {},
      };
    }

    const fieldErrors = zodIssuesToFieldErrors(
      result.error.issues,
      options.shouldUseNativeValidation && options.criteriaMode === 'all',
    );

    return {
      values: {},
      errors: toNestErrors(fieldErrors, options),
    };
  };
}
