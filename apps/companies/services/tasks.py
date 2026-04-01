
# apps/companies/services/tasks.py
from celery import shared_task
from django.db import transaction
from django.conf import settings
from apps.common.services.tasks import send_notification
import logging

logger = logging.getLogger('companies')


@shared_task(bind=True, max_retries=3)
def create_company_background(self, company_data: dict, user_id: int, request_path: str = None):
    """
    Create company in background after validation
    
    Args:
        company_data: Validated company data from serializer
        user_id: ID of the user creating the company
        request_path: Request path for generating links
    """
    try:
        from apps.companies.models.models import Company, CompanyProfile
        from apps.common.models.models import Address
        from django.contrib.contenttypes.models import ContentType
        import secrets
        
        with transaction.atomic():
            # Extract nested data
            addresses_data = company_data.pop('addresses', [])
            profile_data = company_data.pop('profile', None)
            
            # Create company
            company = Company.objects.create(**company_data)
            logger.info(f"Created company {company.id} in background")
            
            # Create addresses
            for address_data in addresses_data:
                Address.objects.create(
                    content_object=company,
                    **address_data
                )
            
            # Create profile if provided
            if profile_data:
                CompanyProfile.objects.create(
                    company=company,
                    **profile_data
                )
            
            # Auto-create HQ branch
            company.auto_create_hq_branch()
            
            # Generate OTP for company verification
            otp_code = str(secrets.randbelow(999999)).zfill(6)
            
            # Get company email for notification
            company_email = None
            if company.profile and company.profile.email:
                company_email = company.profile.email
            
            if company_email:
                # Send notification
                send_notification.delay(
                    recipient_type='company',
                    recipient_id=company.id,
                    notification_type=settings.ADD_COMPANY,
                    context={
                        'company_name': company.trading_name or company.registration_name,
                        'registration_number': company.registration_number,
                        'user_id': user_id,
                    },
                    sender_id=user_id,
                    template_name='company_registration',
                    subject='Company Registration Successful - Fincheck',
                    include_otp=True,
                    otp_code=otp_code,
                    request_path=request_path,
                )
            
            return {
                'success': True,
                'company_id': company.id,
                'message': 'Company created successfully'
            }
            
    except Exception as exc:
        logger.error(f"Company creation failed: {exc}")
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=60, exc=exc)
        return {
            'success': False,
            'error': str(exc)
        }

@shared_task
def create_company_branch_task(data):
    from apps.common.models.models import Address,City, Suburb
    from apps.companies.models.models import Company, CompanyBranch, ContactPerson
    from django.contrib.contenttypes.models import ContentType
    import logging
    logger = logging.getLogger('companies')
    addresses_data = data.pop('addresses', [])
    contacts_data = data.pop('contacts', [])
    company_id = data.pop('company')
    
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return {"success": False, "error": f"Company with ID {company_id} not found."}
    if CompanyBranch.objects.filter(company=company, branch_name=data.get('branch_name')).exists():
        return {"success": False, "error": f"Branch with name {data.get('branch_name')} already exists for this company."}
    branch = CompanyBranch.objects.create(company=company, **data)

    content_type = ContentType.objects.get_for_model(CompanyBranch)
    for address_data in addresses_data:
        if isinstance(address_data.get("city"), int):
            try:
                address_data["city"] = City.objects.get(id=int(address_data["city"]))
            except City.DoesNotExist:
                return {"success": False, "error": f"City with ID {address_data['city']} not found."}
        if isinstance(address_data.get("suburb"), int):
            suburb = address_data.pop("suburb")
            try:
                address_data["suburb"] = Suburb.objects.get(id=suburb)
            except Suburb.DoesNotExist:
                return {"success": False, "error": f"Suburb with ID {suburb} not found."}

        Address.objects.create(
            content_type=content_type,
            object_id=branch.id,
            **address_data
        )
    for contact_data in contacts_data:
        ContactPerson.objects.create(
            company_branch=branch,
            **contact_data
        )

    return {
        "success": True,
        "branch_id": branch.id,
        "branch_name": branch.branch_name,
    }


@shared_task
def send_company_notification(company_id: int, notification_type: str, context: dict, sender_id: int = None):
    """
    Send notification to company
    
    Args:
        company_id: ID of the company
        notification_type: Type of notification
        context: Template context
        sender_id: ID of the sender
    """
    send_notification.delay(
        recipient_type='company',
        recipient_id=company_id,
        notification_type=notification_type,
        context=context,
        sender_id=sender_id,
    )

