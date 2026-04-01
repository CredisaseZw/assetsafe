from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import logging
from apps.common.services.tasks import send_sms

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """Send SMS using the configured SMS service"""

    def handle(self, *args, **options):
        phone_number = '+263717003473'
        message = 'Test message 2 again'
        try:
            send_sms.delay(phone_number, message)
            self.stdout.write(self.style.SUCCESS('SMS sent successfully'))
        except Exception as e:
            logger.error(f"SMS sending failed: {e}")
            self.stderr.write(self.style.ERROR(f"SMS sending failed: {e}"))
