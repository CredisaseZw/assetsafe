# Signal to automatically create HQ branch (place this in signals.py and connect in apps.py)
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.companies.models.models import Company
# apps/companies/signals.py
from django.contrib.contenttypes.models import ContentType
from apps.common.models.models import Address, Document, Note
import logging

logger = logging.getLogger(__name__)
@receiver(post_save, sender=Company)
def create_headquarters_branch_signal(sender, instance, created, **kwargs):
    if created:
        instance.auto_create_hq_branch()


@receiver(pre_save, sender=Address)
@receiver(pre_save, sender=Document)
@receiver(pre_save, sender=Note)
def verify_content_type(sender, instance, **kwargs):
    if instance.content_type_id and not instance.object_id:
        logger.error(f"Missing object_id for {sender.__name__} with content_type {instance.content_type}")
    elif not instance.content_type_id and instance.object_id:
        logger.error(f"Missing content_type for {sender.__name__} with object_id {instance.object_id}")
    elif not instance.content_type_id:
        logger.error(f"Missing both content_type and object_id for {sender.__name__}")