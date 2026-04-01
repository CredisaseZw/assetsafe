

# apps/common/services/notification_service.py
from typing import Dict, Any, Optional
from django.conf import settings
from apps.common.services.tasks import send_notification


class NotificationService:
    """
    Service class for sending notifications
    """
    
    @staticmethod
    def send_company_registration_notification(
        company_id: int,
        user_id: int,
        request_path: str = None,
        include_otp: bool = True,
        otp_code: str = None
    ):
        """Send company registration notification"""
        from apps.companies.models.models import Company
        
        try:
            company = Company.objects.get(id=company_id)
            context = {
                'company_name': company.trading_name or company.registration_name,
                'registration_number': company.registration_number,
                'user_id': user_id,
            }
            
            send_notification.delay(
                recipient_type='company',
                recipient_id=company_id,
                notification_type=settings.ADD_COMPANY,
                context=context,
                sender_id=user_id,
                template_name='company_registration',
                subject='Company Registration Successful - Fincheck',
                include_otp=include_otp,
                otp_code=otp_code,
                request_path=request_path,
            )
            
        except Company.DoesNotExist:
            pass
    
    @staticmethod
    def send_individual_registration_notification(
        individual_id: int,
        user_id: int,
        include_otp: bool = True,
        otp_code: str = None
    ):
        """Send individual registration notification"""
        from apps.individuals.models.models import Individual
        
        try:
            individual = Individual.objects.get(id=individual_id)
            context = {
                'first_name': individual.first_name,
                'last_name': individual.last_name,
                'user_id': user_id,
            }
            
            send_notification.delay(
                recipient_type='individual',
                recipient_id=individual_id,
                notification_type=settings.ADD_INDIVIDUAL,
                context=context,
                sender_id=user_id,
                template_name='individual_registration',
                include_otp=include_otp,
                otp_code=otp_code,
            )
            
        except Individual.DoesNotExist:
            pass
    
    @staticmethod
    def send_payment_receipt(
        recipient_type: str,
        recipient_id: int,
        payment_details: Dict[str, Any],
        sender_id: int = None
    ):
        """Send payment receipt notification"""
        context = {
            'amount': payment_details.get('amount'),
            'payment_method': payment_details.get('payment_method'),
            'transaction_id': payment_details.get('transaction_id'),
            'date': payment_details.get('date'),
        }
        
        send_notification.delay(
            recipient_type=recipient_type,
            recipient_id=recipient_id,
            notification_type=settings.PAYMENT_RECEIPT,
            context=context,
            sender_id=sender_id,
            template_name='payment_receipt',
        )
    
    @staticmethod
    def send_lease_status_update(
        recipient_type: str,
        recipient_id: int,
        lease_details: Dict[str, Any],
        sender_id: int = None
    ):
        """Send lease status update notification"""
        context = {
            'lease_number': lease_details.get('lease_number'),
            'status': lease_details.get('status'),
            'amount_due': lease_details.get('amount_due'),
            'due_date': lease_details.get('due_date'),
        }
        
        send_notification.delay(
            recipient_type=recipient_type,
            recipient_id=recipient_id,
            notification_type=settings.LEASE_STATUS,
            context=context,
            sender_id=sender_id,
            template_name='lease_status_update',
        )