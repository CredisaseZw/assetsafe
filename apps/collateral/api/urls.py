"""
urls.py — Collateral

"""

from rest_framework.routers import SimpleRouter

from .views import CollateralRegistrationViewSet

router = SimpleRouter()
router.register(  # type: ignore
    r"collateral-registrations",
    CollateralRegistrationViewSet,
    basename="collateral-registration",
)

urlpatterns = router.urls  # type: ignore
