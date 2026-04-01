# apps/common/utils/mixins.py
import logging
from django.core.cache import cache

logger = logging.getLogger('cache')

class CachingMixin:
    """
    Enhanced caching mixin with proper invalidation
    """
    def get_cache_timeout(self):
        """Override this to customize cache timeout per view"""
        return self
