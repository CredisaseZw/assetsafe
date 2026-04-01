# apps/common/signals.py
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from apps.common.utils.caching import CacheService
from apps.companies.models.models import Company, CompanyBranch
from apps.common.models.models import Country, Province, City, Suburb, Address
from apps.individuals.models.models import (
    Individual,
    IndividualContactDetail,
    NextOfKin,
    EmploymentDetail,
)
import logging

# from apps.subscriptions.models.models import Services, Subscription, SubscriptionPeriod

logger = logging.getLogger("cache")

MONITORED_MODELS = (
    Company,
    CompanyBranch,
    Country,
    Province,
    City,
    Suburb,
    Address,
    Individual,
    NextOfKin,
    EmploymentDetail,
    IndividualContactDetail,
    # SubscriptionPeriod,
    # Services,
    # Subscription,
)


def invalidate_location_caches(instance):
    """Handle invalidation for location hierarchy models"""
    model_name = instance._meta.model_name.lower()

    CacheService.invalidate_tag(f"locations:{model_name}:list")
    CacheService.invalidate_tag("locations:hierarchy")

    if hasattr(instance, "pk") and instance.pk:
        CacheService.invalidate_tag(f"locations:{model_name}:{instance.pk}")

    if isinstance(instance, Country):
        CacheService.invalidate_tag("locations:countries")
        CacheService.invalidate_tag(f"locations:country:{instance.pk}")

    elif isinstance(instance, Province):
        CacheService.invalidate_tag("locations:provinces")
        CacheService.invalidate_tag(f"locations:province:{instance.pk}")
        if instance.country_id:
            CacheService.invalidate_tag(f"locations:country:{instance.country_id}")

    elif isinstance(instance, City):
        CacheService.invalidate_tag("locations:cities")
        CacheService.invalidate_tag(f"locations:city:{instance.pk}")
        if instance.province_id:
            CacheService.invalidate_tag(f"locations:province:{instance.province_id}")
            if instance.province.country_id:
                CacheService.invalidate_tag(
                    f"locations:country:{instance.province.country_id}"
                )

    elif isinstance(instance, Suburb):
        CacheService.invalidate_tag("locations:suburbs")
        CacheService.invalidate_tag(f"locations:suburb:{instance.pk}")
        if instance.city_id:
            CacheService.invalidate_tag(f"locations:city:{instance.city_id}")
            if instance.city.province_id:
                CacheService.invalidate_tag(
                    f"locations:province:{instance.city.province_id}"
                )
                if instance.city.province.country_id:
                    CacheService.invalidate_tag(
                        f"locations:country:{instance.city.province.country_id}"
                    )


def invalidate_company_caches(instance):
    """Handle invalidation for company models with more comprehensive coverage"""
    model_name = instance._meta.model_name.lower()

    CacheService.invalidate_tag(f"company:{model_name}:list")
    CacheService.invalidate_tag(f"company:{model_name}:search")
    CacheService.invalidate_tag("company:list")
    CacheService.invalidate_tag("company:search")

    if hasattr(instance, "pk") and instance.pk:
        CacheService.invalidate_tag(f"company:{model_name}:{instance.pk}")
        CacheService.invalidate_tag(f"company:{instance.pk}")

        if isinstance(instance, Company):
            CacheService.invalidate_tag(f"company:{instance.pk}:branches")
            CacheService.invalidate_tag("company-branches")

        elif isinstance(instance, CompanyBranch) and hasattr(instance, "company"):
            CacheService.invalidate_tag(f"company:{instance.company.pk}")
            CacheService.invalidate_tag(f"company:{instance.company.pk}:branches")
            CacheService.invalidate_tag("company-branches")

    CacheService.invalidate_tag("choices:location")
    CacheService.invalidate_tag("choices:company")


def invalidate_individual_caches(instance):
    """
    Invalidate cache entries related to the Individual model.
    """
    model_name = instance._meta.model_name.lower()

    # Invalidate list & search cache
    CacheService.invalidate_tag(f"individual:{model_name}:list")
    CacheService.invalidate_tag(f"individual:{model_name}:search")
    CacheService.invalidate_tag("individual:list")
    CacheService.invalidate_tag("individual:search")

    # Invalidate detail & full-details cache if pk is present
    if hasattr(instance, "pk") and instance.pk:
        CacheService.invalidate_tag(f"individual:{model_name}:{instance.pk}")
        CacheService.invalidate_tag(f"individual:{instance.pk}")
        CacheService.invalidate_tag(f"individual:{instance.pk}:full-details")

    CacheService.invalidate_tag("choices:individual")


def invalidate_address_caches(instance):
    """Handle invalidation for address changes"""
    CacheService.invalidate_tag("address:list")

    if hasattr(instance, "pk") and instance.pk:
        CacheService.invalidate_tag(f"address:{instance.pk}")

    if instance.content_object:
        content_type = ContentType.objects.get_for_model(instance.content_object)
        model_name = content_type.model.lower()
        CacheService.invalidate_tag(f"{model_name}:{instance.content_object.pk}")
        CacheService.invalidate_tag(
            f"{model_name}:{instance.content_object.pk}:addresses"
        )


def invalidate_subscription_caches(instance):
    """Handle invalidation for subscription-related models"""
    model_name = instance._meta.model_name.lower()

    CacheService.invalidate_tag("subscription:list")
    CacheService.invalidate_tag("subscription:search")
    CacheService.invalidate_tag("services:list")
    CacheService.invalidate_tag("period:list")

    if hasattr(instance, "pk") and instance.pk:
        CacheService.invalidate_tag(f"subscription:{model_name}:{instance.pk}")
        CacheService.invalidate_tag(f"subscription:{instance.pk}")

    CacheService.invalidate_tag("choices:subscription")


@receiver([post_save, post_delete])
def invalidate_model_cache(sender, instance, **kwargs):
    """
    Central signal handler for all model changes.
    """
    if sender not in MONITORED_MODELS:
        return

    try:
        logger.debug(
            f"Invalidating caches for {sender.__name__} ID {getattr(instance, 'pk', 'new')}"
        )
        if sender in (Company, CompanyBranch):
            invalidate_company_caches(instance)
        elif sender in (Country, Province, City, Suburb):
            invalidate_location_caches(instance)
        elif sender in (
            Individual,
            NextOfKin,
            EmploymentDetail,
            IndividualContactDetail,
        ):
            invalidate_individual_caches(instance)
        elif sender == Address:
            invalidate_address_caches(instance)
        elif sender in (Subscription, Services, SubscriptionPeriod):
            invalidate_subscription_caches(instance)

        logger.debug(
            f"Successfully invalidated caches for {sender.__name__} ID {getattr(instance, 'pk', 'new')}"
        )

    except Exception as e:
        logger.error(
            f"Failed to invalidate caches for {sender.__name__}: {e}", exc_info=True
        )
        CacheService.invalidate_tag("*")


@receiver(m2m_changed)
def invalidate_m2m_cache(sender, instance, action, **kwargs):
    """
    Handle cache invalidation for many-to-many relationship changes.
    """
    if action in ["post_add", "post_remove", "post_clear"]:
        invalidate_model_cache(sender=instance.__class__, instance=instance)
