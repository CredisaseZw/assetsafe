"""
urls.py — Asset Management

"""

from rest_framework.routers import SimpleRouter

from .views import AssetRegistrationViewSet

router = SimpleRouter()
router.register(  # type: ignore
    r"asset-registrations",
    AssetRegistrationViewSet,
    basename="asset-registration",
)

urlpatterns = router.urls  # type: ignore
