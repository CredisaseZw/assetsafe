"""
urls.py — Hire Purchase

"""

from rest_framework.routers import SimpleRouter

from .views import HirePurchaseRegistrationViewSet

router = SimpleRouter()
router.register(  # type: ignore
    r"hire-purchase-registrations",
    HirePurchaseRegistrationViewSet,
    basename="hire-purchase-registration",
)

urlpatterns = router.urls  # type: ignore
