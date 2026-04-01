"""
urls.py — AssetSafe

"""

from rest_framework.routers import DefaultRouter

from .views import (
    AssetRegistrationViewSet,
    CollateralRegistrationViewSet,
    HirePurchaseRegistrationViewSet,
)

router = DefaultRouter()
router.register(  # type: ignore
    r"asset-registrations",
    AssetRegistrationViewSet,
    basename="asset-registration",
)
router.register(  # type: ignore
    r"collateral-registrations",
    CollateralRegistrationViewSet,
    basename="collateral-registration",
)
router.register(  # type: ignore
    r"hire-purchase-registrations",
    HirePurchaseRegistrationViewSet,
    basename="hire-purchase-registration",
)

urlpatterns = router.urls  # type: ignore
