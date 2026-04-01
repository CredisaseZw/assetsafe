
def check_rentsafe_subscription(client, service_code):
    from apps.subscriptions.models import Services, Subscription
    from apps.leases.models import Lease
    """
    Check if a client has an active subscription for a given service code.
    """
    try:
        service = Services.objects.get(code=service_code)
        active_subscription = Subscription.objects.filter(
            client=client,
            service=service,
            is_activated=True
        ).last()
        return bool(
            active_subscription
            and (int(active_subscription.open_slots) > 0)
        )
    except Services.DoesNotExist:
        return False
    except Exception as e:
        return False