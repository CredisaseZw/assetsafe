"""
Audit service — helpers for creating AuditLog entries.

Call ``create_audit_log`` from any view or service layer to record a
sensitive operation in the database and write it to the appropriate
per-app log file.
"""

from __future__ import annotations

import logging

from apps.users.models.audit import AuditLog


def _get_client_ip(request) -> str | None:
    """Extract the real client IP, respecting X-Forwarded-For."""
    if not request:
        return None
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def create_audit_log(
    request,
    action: str,
    resource_type: str | None = None,
    resource_id: int | None = None,
    details: dict | None = None,
    success: bool = True,
    logger: logging.Logger | None = None,
) -> AuditLog:
    """
    Persist an AuditLog row and emit an INFO-level log message to the
    supplied ``logger`` (typically the calling module's logger so that
    each app's audit lines land in its own rotating log file).

    Parameters
    ----------
    request:
        The current DRF/Django request.  May be ``None`` for programmatic
        calls (e.g. from a Celery task).
    action:
        Human-readable description of what happened, e.g.
        ``"asset_registration.create"``.
    resource_type:
        Model class name of the affected object, e.g. ``"AssetRegistration"``.
    resource_id:
        Primary key of the affected object.
    details:
        Arbitrary JSON-serialisable dict with extra context.
    success:
        Whether the operation completed successfully.
    logger:
        A :class:`logging.Logger` instance.  When provided, an INFO entry
        is written to that logger so it appears in the app-specific log file
        configured in ``LOGGING``.
    """
    user = (
        request.user
        if request and hasattr(request, "user") and request.user.is_authenticated
        else None
    )
    ip_address = _get_client_ip(request)
    user_agent = (
        request.META.get("HTTP_USER_AGENT", "") if request else ""
    )

    log_entry = AuditLog.objects.create(
        created_by=user,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
        success=success,
    )

    if logger is not None:
        user_id = user.pk if user else "anonymous"
        logger.info(
            "AUDIT action=%s resource_type=%s resource_id=%s user=%s success=%s",
            action,
            resource_type,
            resource_id,
            user_id,
            success,
        )

    return log_entry
