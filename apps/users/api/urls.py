from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.api.views import (
    LoginView,CurrentUserView,
    UserViewSet, RoleViewSet,
    LogoutView, RefreshTokenView,
    CheckCSRFView
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('check-csrf/', CheckCSRFView.as_view(), name='check-csrf'),
    path('', include(router.urls)),
]