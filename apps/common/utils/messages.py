from typing import Dict, Any
from django.utils import timezone
from datetime import datetime


def generate_sms_message(template_name: str, context: Dict[str, Any]) -> str:
    """
    Generate SMS message content based on a template and context.
    """
    # Template definitions for all notification types
    templates = {
        # Lease-related templates
        "LEASE_CREATED": "Hi {tenant_name}, lease {lease_id} created for {unit} at {property} by {created_by}. Rent: {currency} {rent_amount}/{payment_frequency}. Due: {due_day}th. Start: {start_date}. Your payment status is {payment_status} with opening balance {currency} {opening_balance}",
        "LEASE_UPDATED": "Hi {tenant_name}, lease {lease_id} updated. Check portal for details.",
        "LEASE_TERMINATED": "Hi {tenant_name}, lease {lease_id} terminated on {effective_date}. Reason: {update_reason}",
        "LEASE_RENEWED": "Hi {tenant_name}, lease {lease_id} renewed until {end_date}. Rent: {currency} {rent_amount}",
        # Payment-related templates
        "PAYMENT_RECEIVED": "Hi {tenant_name}, payment of {currency} {amount} received for {lease_id}. Balance: {currency} {balance}. Status: {risk_status}",
        "PAYMENT_DUE_REMINDER": "Hi {tenant_name}, rent for {lease_id} due. Amount: {currency} {amount}. Due: {due_day}th. Balance: {currency} {balance}",
        "PAYMENT_OVERDUE": "Hi {tenant_name}, rent for {lease_id} overdue. Amount due: {currency} {amount}. Please pay immediately",
        # Risk status templates
        "RISK_STATUS_UPDATED": "Hi {tenant_name}, risk status for {lease_id} {risk_improved} to {risk_status}. Balance: {currency} {balance}. Last payment: {last_payment_date}",
        # Status update templates
        "LEASE_STATUS": "Hi {tenant_name}, lease {lease_id} status changed to {new_status_display}. Previous: {old_status_display}. Reason: {update_reason}",
        # Renewal templates
        "LEASE_RENEWAL_REMINDER": "Hi {tenant_name}, lease {lease_id} expires in {days_until_expiry} days on {end_date}. Balance: {currency} {balance}. Contact us to renew",
        # Default fallback template
        "DEFAULT": "Hi {tenant_name}, notification regarding {lease_id}. Please check portal for details",
    }

    # Get the appropriate template
    template = templates.get(template_name)
    if not template:
        # Fallback to default if template not found
        template = templates["DEFAULT"]

    try:
        # Ensure required context variables have defaults
        context.setdefault("tenant_name", "Tenant")
        context.setdefault("lease_id", "N/A")
        context.setdefault("currency", "USD")
        context.setdefault("get_latest_balance", "0.00")
        context.setdefault("client_name", "N/A")
        context.setdefault("payment_status", "Low Risk")
        context.setdefault("amount", "0.00")
        context.setdefault("balance", "0.00")
        context.setdefault("risk_status", "N/A")
        context.setdefault("update_reason", "No reason provided")

        # Format the message
        message = template.format(**context)

        # Truncate if too long (SMS limit is typically 160 characters)
        if len(message) > 160:
            message = message[:157] + "..."

        return message

    except KeyError as e:
        # Handle missing context variables gracefully
        missing_var = str(e).strip("'")
        return f"Hi {context.get('tenant_name', 'Tenant')}, important notification regarding {context.get('lease_id', 'your lease')}. Please check portal for details."

    # Add detailed lease data for email templates


def prepare_lease_creation_context(lease, tenant=None, for_email=False):
    """
    Prepare context for lease creation messages
    """
    from apps.leases.utils.utils import get_tenant_display
    from apps.leases.api.serializers import LeaseDetailSerializer

    # Get start and end dates safely
    start_date = getattr(lease, "start_date", None)
    end_date = getattr(lease, "end_date", None)

    context = {
        "tenant_name": get_tenant_display(tenant) if tenant else "Tenant",
        "lease_id": getattr(lease, "lease_id", "N/A"),
        "property": getattr(
            getattr(getattr(lease, "unit", None), "property", None), "name", "N/A"
        ),
        "unit": getattr(getattr(lease, "unit", None), "unit_number", "N/A"),
        "currency": getattr(getattr(lease, "currency", None), "currency_code", "USD"),
        "start_date": start_date.strftime("%d-%b-%Y") if start_date else "N/A",
        "end_date": end_date.strftime("%d-%b-%Y") if end_date else "N/A",
        "due_day": getattr(lease, "due_day_of_month", 1),
        "payment_frequency": getattr(lease, "payment_frequency", "Monthly"),
        "created_by": getattr(lease, "client_name", "Admin"),
        "client_email": getattr(
            getattr(lease, "managing_client", None), "email", "N/A"
        ),
        "lease_status": getattr(lease, "payment_status", "N/A"),
        "opening_balance": f"{getattr(lease, 'get_latest_balance', 0):.2f}",
    }

    # Get rent amount from charges
    rent_amount = "0.00"
    if hasattr(lease, "charges"):
        if rent_charge := lease.charges.filter(
            charge_type="RENT", is_active=True
        ).first():
            rent_amount = f"{rent_charge.amount:.2f}"
    context["rent_amount"] = rent_amount

    if for_email:
        context["lease"] = LeaseDetailSerializer(lease).data

    return context


def prepare_lease_payment_context(
    lease, amount, payment_date=None, tenant=None, for_email=False
):
    """
    Prepare context for lease payment messages
    """
    from apps.leases.utils.utils import get_tenant_display
    from apps.leases.api.serializers import LeaseDetailSerializer

    if isinstance(payment_date, str):
        try:
            payment_date = datetime.fromisoformat(payment_date)
        except ValueError:
            payment_date = datetime.strptime(payment_date, "%Y-%m-%d")

    if not payment_date:
        payment_date = timezone.now()

    context = {
        "tenant_name": get_tenant_display(tenant) if tenant else "Tenant",
        "lease_id": getattr(lease, "lease_id", "N/A"),
        "property": getattr(
            getattr(getattr(lease, "unit", None), "property", None), "name", "N/A"
        ),
        "unit": getattr(getattr(lease, "unit", None), "unit_number", "N/A"),
        "amount": f"{float(amount):.2f}",
        "currency": getattr(getattr(lease, "currency", None), "currency_code", "USD"),
        "balance": f"{getattr(lease, 'current_balance', 0):.2f}",
        "payment_status": getattr(lease, "payment_status", "N/A"),
        "payment_date": payment_date.strftime("%d-%b-%Y") if payment_date else "N/A",
        "created_by": getattr(lease, "client_name", "Admin"),
        "client_email": getattr(
            getattr(lease, "managing_client", None), "email", "N/A"
        ),
        "due_day": getattr(lease, "due_day_of_month", 1),
    }

    if for_email:
        context["lease"] = LeaseDetailSerializer(lease).data

    return context


def prepare_lease_status_context(
    lease, new_status, status_display, reason=None, tenant=None
):
    """Prepare context for lease status update messages"""
    from apps.leases.utils.utils import get_tenant_display

    return {
        "tenant_name": get_tenant_display(tenant) if tenant else "Tenant",
        "lease_id": getattr(lease, "lease_id", "N/A"),
        "new_status": new_status,
        "new_status_display": status_display.get(new_status, new_status),
        "old_status_display": status_display.get(getattr(lease, "status", ""), "N/A"),
        "update_reason": reason or "No reason provided",
        "effective_date": timezone.now().strftime("%d-%b-%Y"),
    }


def prepare_risk_status_context(
    lease, old_risk_status, last_payment_date=None, risk_improved=False, tenant=None
):
    """Prepare context for risk status update messages"""
    from apps.leases.utils.utils import get_tenant_display

    return {
        "tenant_name": get_tenant_display(tenant) if tenant else "Tenant",
        "lease_id": getattr(lease, "lease_id", "N/A"),
        "currency": getattr(getattr(lease, "currency", None), "currency_code", "USD"),
        "balance": f"{getattr(lease, 'current_balance', 0):.2f}",
        "risk_status": getattr(lease, "risk_level", "N/A"),
        "old_risk_status": old_risk_status,
        "last_payment_date": (
            last_payment_date.strftime("%d-%b-%Y") if last_payment_date else "Never"
        ),
        "risk_improved": "improved" if risk_improved else "worsened",
    }


def prepare_lease_renewal_context(lease, days_until_expiry, tenant=None):
    """Prepare context for lease renewal reminder messages"""
    from apps.leases.utils.utils import get_tenant_display
    from django.conf import settings

    # Get notice period from settings or lease
    notice_period_days = getattr(
        lease, "notice_period_days", getattr(settings, "DEFAULT_NOTICE_PERIOD_DAYS", 30)
    )

    return {
        "tenant_name": get_tenant_display(tenant) if tenant else "Tenant",
        "lease_id": getattr(lease, "lease_id", "N/A"),
        "end_date": getattr(lease, "end_date", timezone.now().date()).strftime(
            "%d-%b-%Y"
        ),
        "days_until_expiry": days_until_expiry,
        "notice_period_days": notice_period_days,
        "currency": getattr(getattr(lease, "currency", None), "currency_code", "USD"),
        "balance": f"{getattr(lease, 'current_balance', 0):.2f}",
        "risk_status": getattr(lease, "risk_level", "N/A"),
    }
