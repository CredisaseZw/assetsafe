# users/utils/cookies.py
from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


# users/utils/cookies.py
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)

def set_jwt_cookies(response, access_token, refresh_token=None):
    """
    Set JWT tokens as HTTP-only cookies in the response.
    Handles both HttpResponse and Response objects properly.
    """
    try:
        # If it's a DRF Response, convert to Django HttpResponse for cookie operations
        if hasattr(response, 'accepted_renderer'):
            # It's a DRF Response, we need to handle it differently
            data = response.data
            status_code = response.status_code
            content_type = response.get('Content-Type', 'application/json')
            
            # Create a new HttpResponse with the same data
            http_response = HttpResponse(
                json.dumps(data),
                status=status_code,
                content_type=content_type
            )
        else:
            # It's already an HttpResponse
            http_response = response
        
        # Set access token cookie
        http_response.set_cookie(
            key=settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token'),
            value=access_token,
            max_age=int(settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=60)).total_seconds()),
            secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
            httponly=settings.SIMPLE_JWT.get('AUTH_COOKIE_HTTP_ONLY', True),
            samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax'),
            path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
            domain=settings.SIMPLE_JWT.get('AUTH_COOKIE_DOMAIN', None),
        )
        
        # Set refresh token cookie if provided
        if refresh_token:
            http_response.set_cookie(
                key=settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'),
                value=refresh_token,
                max_age=int(settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME', timedelta(days=7)).total_seconds()),
                secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
                httponly=settings.SIMPLE_JWT.get('AUTH_COOKIE_HTTP_ONLY', True),
                samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax'),
                path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
                domain=settings.SIMPLE_JWT.get('AUTH_COOKIE_DOMAIN', None),
            )
        
        return http_response
        
    except Exception as e:
        logger.error(f"Error setting JWT cookies: {str(e)}")
        raise

def delete_jwt_cookies(response):
    """
    Delete JWT cookies from the response (for logout).
    """
    try:
        # If it's a DRF Response, convert to Django HttpResponse
        if hasattr(response, 'accepted_renderer'):
            data = response.data
            status_code = response.status_code
            content_type = response.get('Content-Type', 'application/json')
            
            http_response = HttpResponse(
                json.dumps(data),
                status=status_code,
                content_type=content_type
            )
        else:
            http_response = response
        
        # Delete access token cookie
        http_response.delete_cookie(
            key=settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token'),
            path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
            domain=settings.SIMPLE_JWT.get('AUTH_COOKIE_DOMAIN', None),
        )
        
        # Delete refresh token cookie
        http_response.delete_cookie(
            key=settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'),
            path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
            domain=settings.SIMPLE_JWT.get('AUTH_COOKIE_DOMAIN', None),
        )
        
        return http_response
        
    except Exception as e:
        logger.error(f"Error deleting JWT cookies: {str(e)}")
        raise

def create_response_with_cookies(data, status_code, access_token=None, refresh_token=None):
    """
    Create a response with JWT cookies set.
    """
    response = HttpResponse(
        json.dumps(data),
        status=status_code,
        content_type='application/json'
    )
    
    if access_token:
        response = set_jwt_cookies(response, access_token, refresh_token)
    
    return response

# Keep the other utility functions as they are
def get_tokens_from_request(request):
    """
    Extract JWT tokens from request cookies.
    """
    return {
        'access_token': request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token')),
        'refresh_token': request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'))
    }

def has_valid_jwt_cookies(request):
    """
    Check if request has valid JWT cookies.
    """
    tokens = get_tokens_from_request(request)
    return bool(tokens['access_token'])

