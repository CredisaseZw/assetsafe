
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.companies.api.views import CompanyViewSet, CompanyBranchViewSet # Import both ViewSets

router = DefaultRouter()

router.register(r'companies', CompanyViewSet, basename='company') 

router.register(r'branches', CompanyBranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
]