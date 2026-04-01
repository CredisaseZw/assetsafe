import logging
import json
import time
from django.http import JsonResponse

logger = logging.getLogger('companies')

class DetailedErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        error_data = {
            'path': request.path,
            'method': request.method,
            'exception_type': str(type(exception)),
            'exception_message': str(exception),
            'request_data': request.POST if request.method == 'POST' else request.GET,
            'request_body': request.body.decode('utf-8', errors='replace') if request.body else None,
            'stack_trace': self._get_stack_trace(exception)
        }
        
        logger.error("Detailed error occurred:\n" + json.dumps(error_data, indent=2))
        
        if request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'Internal Server Error',
                'detail': str(exception),
                'exception_type': str(type(exception))
            }, status=500)
        return None

    def _get_stack_trace(self, exception):
        import traceback
        return traceback.format_exc()