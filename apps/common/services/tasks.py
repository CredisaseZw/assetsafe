
# apps/common/tasks.py
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.utils.html import strip_tags
from urllib.parse import urlparse
import requests
import logging
from typing import Union, Dict, Any, Optional
import contextlib
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from importlib import import_module
import re


logger = logging.getLogger(__name__)

@shared_task()
def send_notification(
    recipient_type: str,
    recipient_id: int,
    notification_type: str,
    context: Dict[str, Any],
    sender_id: Optional[int] = None,
    template_name: Optional[str] = None,
    sms_template_name: Optional[str] = None,
    subject: Optional[str] = None,
    message: Optional[str] = None,
    include_otp: bool = False,
    otp_code: Optional[str] = None,
    request_path: Optional[str] = None,
    is_creditor: bool = False,
    force_method: Optional[str] = None,  # 'sms', 'email', or None for auto
):
    """
    Unified notification service for both SMS and Email
    
    Args:
        recipient_type: 'individual' or 'company' or 'user'
        recipient_id: ID of the recipient
        notification_type: Type of notification (LEASE_CREATED, PAYMENT_RECEIVED, etc.)
        context: Template context data
        sender_id: ID of the user sending the notification
        template_name: Email template name (optional)
        sms_template_name: SMS template name (optional)
        subject: Email subject (optional)
        message: Direct message (optional)
        include_otp: Whether to include OTP in the message
        otp_code: OTP code if applicable
        request_path: Request path for generating links
        is_creditor: Whether the sender is a creditor
        force_method: Force a specific delivery method ('sms' or 'email')
    """
    try:
        # Get recipient details based on type
        contact_method = None
        use_sms = False
        recipient_obj = None
        if recipient_type == 'individual':
            from apps.individuals.models.models import Individual
            recipient_obj = Individual.objects.get(id=recipient_id)
            # Try mobile phone first
            contact_method = recipient_obj.phone
            use_sms = bool(contact_method and not force_method == 'email')
            # If no phone or forced email, try individual's email
            if not contact_method or force_method == 'email':
                contact_method = recipient_obj.email
                use_sms = False
                    
        elif recipient_type == 'company':
            from apps.companies.models.models import CompanyBranch
            recipient_obj = CompanyBranch.objects.get(id=recipient_id)
            # Get primary contact email from company profile
            contact_method= recipient_obj.email
            if not contact_method and hasattr(recipient_obj, 'contacts'):
                primary_contact = recipient_obj.contacts.filter(is_primary=True).first()
                if primary_contact:
                    contact_method = primary_contact.email
                else:
                    # Fallback to context user email or company email
                    contact_method = context.get('user', {}).get('email', recipient_obj.email)
            use_sms = False 
            
        elif recipient_type == 'user':
            from django.contrib.auth import get_user_model
            User = get_user_model()
            recipient_obj = User.objects.get(id=recipient_id)
            # Try email first for users
            contact_method = recipient_obj.email
            use_sms = False
            # Fallback to phone if email not available and SMS is forced
            if not contact_method and force_method == 'sms':
                if hasattr(recipient_obj, 'phone'):
                    contact_method = recipient_obj.phone
                    use_sms = True
                elif hasattr(recipient_obj, 'profile') and hasattr(recipient_obj.profile, 'phone'):
                    contact_method = recipient_obj.profile.phone
                    use_sms = True
        if not contact_method:
            raise ValueError(f"No contact method found for {recipient_type} {recipient_id}")

        # Override method if force_method is specified
        if force_method:
            use_sms = (force_method.lower() == 'sms')
            # If forcing SMS but we only have email, try to get phone
            if use_sms and '@' in contact_method:
                if recipient_type == 'individual' and recipient_obj and recipient_obj.phone:
                    contact_method = recipient_obj.phone
                else:
                    raise ValueError(f"Cannot send SMS to {recipient_type} {recipient_id} - no phone available")

        # Prepare message content
        email_content = message
        sms_content = message
        
        # Use templates if provided
        if template_name and not use_sms:
            try:
                email_content = render_to_string(f'emails/{template_name}.html', context)
            except TemplateDoesNotExist:
                logger.warning(f"Email template {template_name} not found, using plain text")
        
        if sms_template_name and use_sms:
            try:
                sms_content = render_to_string(f'sms/{sms_template_name}.txt', context)
            except TemplateDoesNotExist:
                logger.warning(f"SMS template {sms_template_name} not found, using plain text")

        # Handle OTP if needed
        if include_otp and otp_code:
            if use_sms:
                sms_content = f"{sms_content} {otp_code}"
            elif request_path:
                parsed_url = urlparse(request_path)
                url_path = f"{parsed_url.scheme}://{parsed_url.netloc}"
                if otp_link := _generate_otp_link(
                    url_path, otp_code, recipient_id, notification_type
                ):
                    email_content += f"\n\nClick here to verify: {otp_link}"

        # Send notification
        if use_sms:
            success = send_sms(contact_method,sms_template_name, context)
        else:
            success = send_email(
                contact_method, 
                subject or _get_default_subject(notification_type, context),
                email_content,
                is_html=bool(template_name and not use_sms)
            )

        if not success:
            raise Exception(f"Failed to send {('SMS' if use_sms else 'Email')} notification")


        return {
            "success": True, 
            "method": "SMS" if use_sms else "Email",
            "recipient": str(recipient_obj) if recipient_obj else f"{recipient_type}_{recipient_id}"
        }

    except Exception as exc:
        logger.error(f"Notification failed: {exc}", exc_info=True)
        return {
            "success": False,
            "error": str(exc)
        }


@shared_task()
def send_sms(phone_number, template_name: str, context: Dict[str, Any]) -> bool:
    """
    Send SMS using the configured SMS service with retry logic
    
    Args:
        phone_number: Recipient phone number (string or list)
        template_name: Name of the SMS template to use
        context: Context variables for the template
    """
    try:
        # Handle phone number if it's a list
        if isinstance(phone_number, list):
            if phone_number:
                phone_number = phone_number[0]  # Take the first phone number
            else:
                raise ValueError("Empty phone number list provided")
        

        # Generate SMS message
        from apps.common.utils.messages import generate_sms_message
        message = generate_sms_message(template_name, context)
        
        # Truncate message if too long (SMS limit is typically 160 characters)
        if len(message) > 160:
            message = message[:157] + "..."
        
        url = "http://sms.vas.co.zw/client/api/sendmessage?"
        params = {
            "apikey": settings.SMS_API_KEY,
            "mobiles": phone_number,
            "sms": message,
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        # Log successful SMS delivery
        logger.info(f"SMS sent to {phone_number}: {message[:50]}...")
        return True
        
    except Exception as e:
        logger.error(f"SMS sending failed to {phone_number}: {e}")
        return False


@shared_task()
def send_email( email: str, subject: str, message: str, is_html: bool = False) -> bool:
    """Send email using Django's email backend with retry logic"""
    try:
        mail = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
            reply_to=[settings.DEFAULT_REPLY_TO_EMAIL] if hasattr(settings, 'DEFAULT_REPLY_TO_EMAIL') else None
        )
        
        if is_html:
            mail.content_subtype = "html"
            
        mail.send(fail_silently=False)
        
        # Log successful email delivery
        logger.info(f"Email sent to {email}: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Email sending failed to {email}: {e}")
        return False


def _get_default_subject(notification_type: str, context: Dict[str, Any] = None) -> str:
    """Get default email subject based on notification type with context support"""
    context = context or {}
    
    # Lease-related subjects
    lease_subjects = {
        settings.LEASE_CREATED: "New Lease Created - {platform_name}",
        settings.LEASE_UPDATED: "Lease Updated - {platform_name}",
        settings.LEASE_TERMINATED: "Lease Terminated - {platform_name}",
        settings.PAYMENT_RECEIVED: "Payment Received - {platform_name}",
        settings.RISK_STATUS_UPDATED: "Risk Status Update - {platform_name}",
        settings.LEASE_RENEWAL_REMINDER: "Lease Renewal Reminder - {platform_name}",
    }
    
    # Default subjects if not found in lease-specific ones
    subjects = {
        settings.ADD_COMPANY: "Company Registration - {platform_name}",
        settings.ADD_INDIVIDUAL: "Individual Registration - {platform_name}",
        settings.ADD_COMP_LEASE: "New Lease - {platform_name}",
        settings.PAYMENT_RECEIPT: "Payment Receipt - {platform_name}",
        settings.LEASE_STATUS: "Lease Status Update - {platform_name}",
        settings.CREDIT_CHECK: "Credit Check - {platform_name}",
        settings.LEASE_CREATED: "New Lease Created - {platform_name}",
        settings.PAYMENT_RECEIVED: "Payment Received - {platform_name}",
        settings.RISK_STATUS_UPDATED: "Risk Status Update - {platform_name}",
        settings.LEASE_RENEWAL_REMINDER: "Lease Renewal Reminder - {platform_name}",
    }
    
    # Try lease-specific first, then fall back to general
    subject_template = lease_subjects.get(notification_type) or subjects.get(notification_type, "Notification - {platform_name}")
    
    # Format with context
    platform_name = context.get('platform_name', settings.PLATFORM_NAME if hasattr(settings, 'PLATFORM_NAME') else 'Fincheck')
    
    return subject_template.format(
        platform_name=platform_name,
        **context
    )


def _generate_otp_link(url_path: str, otp_code: str, recipient_id: int, notification_type: str) -> Optional[str]:
    """Generate OTP verification link based on notification type"""
    import random
    import string
    
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    
    link_patterns = {
        settings.ADD_COMPANY: f"{url_path}/clients/company-verify-otp/{random_string}T{otp_code}L{random_string}!{recipient_id}B/",
        settings.ADD_COMP_LEASE: f"{url_path}/clients/cl-verify-lease/{random_string}T{otp_code}L{random_string}!{recipient_id}B/",
    }
    
    return link_patterns.get(notification_type)


def _save_otp(otp_code: str, otp_type: str, request_user: int, requested_user: int, requested_user_type: str):
    """Save OTP to database"""
    try:
        from apps.communications.models.models import OTP 
        OTP.objects.create(
            otp_code=otp_code,
            otp_type=otp_type,
            request_user_id=request_user,
            requested_user=requested_user,
            requested_user_type=requested_user_type,
        )
    except Exception as e:
        logger.error(f"Failed to save OTP: {e}")


def _add_to_communication_history(
    user_id: int, 
    client_id: int, 
    message: str, 
    is_sms: bool, 
    is_email: bool, 
    is_creditor: bool,
    notification_type: str
):
    """Add message to communication history"""
    # try:
    #     from apps.communications.utils import add_msg_to_comms_hist 
    #     add_msg_to_comms_hist(
    #         user_id=user_id,
    #         client_id=client_id,
    #         message=message,
    #         is_sms=is_sms,
    #         is_email=is_email,
    #         is_creditor=is_creditor,
    #         notification_type=notification_type
    #     )
    # except Exception as e:
    logger.error(f"Failed to add to communication history: {e}")
@shared_task(bind=True)
def create_object_task(self, serializer_class_path, model_name, data, context):
    """
    Async object creation with proper serializer/model loading
    """
    try:
        module_path, class_name = serializer_class_path.rsplit('.', 1)
        module = import_module(module_path)
        serializer_class = getattr(module, class_name)
        
        model = apps.get_model(model_name)
        
        user = apps.get_model('users.User').objects.get(pk=context['user_id'])
        context = {'request': context.get('request', {}), 'user': user}
        
        serializer = serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        
        if hasattr(model, 'user'):
            instance = serializer.save(user=user)
        else:
            instance = serializer.save()
            
        return {
            'status': 'SUCCESS',
            'instance_id': instance.id,
            'content_type_id': ContentType.objects.get_for_model(model).id
        }
    except Exception as e:
        logger.error(f"Async create failed: {str(e)}")
        return {
            'status': 'FAILURE',
            'error': str(e)
        }

@shared_task(bind=True)
def update_object_task(self, serializer_class_path, model_name, instance_id, data, context):
    """
    Async object update with proper serializer/model loading
    """
    try:
        module_path, class_name = serializer_class_path.rsplit('.', 1)
        module = import_module(module_path)
        serializer_class = getattr(module, class_name)
        
        model = apps.get_model(model_name)
        instance = model.objects.get(pk=instance_id)
        
        user = apps.get_model('users.User').objects.get(pk=context['user_id'])
        context = {'request': context.get('request', {}), 'user': user}
        
        serializer = serializer_class(instance, data=data, context=context, partial=True)
        serializer.is_valid(raise_exception=True)
        
        if hasattr(model, 'user'):
            serializer.save(user=user)
        else:
            serializer.save()
            
        return {
            'status': 'SUCCESS',
            'instance_id': instance_id
        }
    except Exception as e:
        logger.error(f"Async update failed: {str(e)}")
        return {
            'status': 'FAILURE',
            'error': str(e)
        }

def _generate_otp_link(url_path: str, otp_code: str, recipient_id: int, notification_type: str) -> Optional[str]:
    """Generate OTP verification link based on notification type"""
    import random
    import string
    
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    
    link_patterns = {
        settings.ADD_COMPANY: f"{url_path}/clients/company-verify-otp/{random_string}T{otp_code}L{random_string}!{recipient_id}B/",
        settings.ADD_COMP_LEASE: f"{url_path}/clients/cl-verify-lease/{random_string}T{otp_code}L{random_string}!{recipient_id}B/",
    }
    
    return link_patterns.get(notification_type)


def _get_default_subject(notification_type: str) -> str:
    """Get default email subject based on notification type"""
    subjects = {
        settings.ADD_COMPANY: "Company Registration - Fincheck",
        settings.ADD_INDIVIDUAL: "Individual Registration - Fincheck",
        settings.ADD_COMP_LEASE: "New Lease - Fincheck",
        settings.PAYMENT_RECEIPT: "Payment Receipt - Fincheck",
        settings.LEASE_STATUS: "Payment Status Update - Fincheck",
        settings.CREDIT_CHECK: "Credit Check - Fincheck",
    }
    return subjects.get(notification_type, "Notification - Fincheck")


def _save_otp(otp_code: str, otp_type: str, request_user: int, requested_user: int, requested_user_type: str):
    """Save OTP to database"""
    try:
        from apps.communications.models.models import OTP 
        OTP.objects.create(
            otp_code=otp_code,
            otp_type=otp_type,
            request_user=request_user,
            requested_user=requested_user,
            requested_user_type=requested_user_type,
        )
    except Exception as e:
        logger.error(f"Failed to save OTP: {e}")


def _add_to_communication_history(user_id: int, client_id: int, message: str, is_sms: bool, is_email: bool, is_creditor: bool):
    """Add message to communication history"""
    return True
    try:
        from apps.communications.utils import add_msg_to_comms_hist 
        add_msg_to_comms_hist(
            user_id=user_id,
            client_id=client_id,
            message=message,
            is_sms=is_sms,
            is_email=is_email,
            is_creditor=is_creditor,
        )
    except Exception as e:
        logger.error(f"Failed to add to communication history: {e}")


@shared_task
def cleanup_expired_otps():
    """Clean up expired OTP records"""
    try:
        from apps.common.models.models import OTP
        from django.utils import timezone
        from datetime import timedelta
        
        expired_time = timezone.now() - timedelta(hours=24)
        deleted_count = OTP.objects.filter(created_at__lt=expired_time).delete()[0]
        logger.info(f"Cleaned up {deleted_count} expired OTP records")
        return deleted_count
    except Exception as e:
        logger.error(f"Failed to clean up expired OTPs: {e}")
        return 0

