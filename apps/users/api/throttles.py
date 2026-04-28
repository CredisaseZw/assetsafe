"""Custom throttle classes for user-facing API endpoints."""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """
    Throttle for the login endpoint: 10 requests per minute per IP address.
    Scope maps to THROTTLE_RATES['login'] in REST_FRAMEWORK settings.
    """

    scope = "login"
