# apps/common/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.common.api.views import LocationViewSet,SuburbViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'suburbs', SuburbViewSet, basename='suburb')

urlpatterns = [
    
    path('locations/countries/', LocationViewSet.as_view({'get': 'countries', 'post': 'countries'}), name='country-list'),
    path('locations/countries/<int:pk>/', LocationViewSet.as_view({'get': 'country_detail', 'put': 'country_detail', 'patch': 'country_detail', 'delete': 'country_detail'}), name='country-detail'),
    
    path('locations/provinces/', LocationViewSet.as_view({'get': 'provinces', 'post': 'create_province'}), name='province-list'),
    path('locations/provinces/<int:pk>/', LocationViewSet.as_view({'get': 'province_detail', 'put': 'province_detail', 'patch': 'province_detail', 'delete': 'province_detail'}), name='province-detail'),
    
    path('locations/cities/', LocationViewSet.as_view({'get': 'cities', 'post': 'create_city'}), name='city-list'),
    path('locations/cities/<int:pk>/', LocationViewSet.as_view({'get': 'city_detail', 'put': 'city_detail', 'patch': 'city_detail', 'delete': 'city_detail'}), name='city-detail'),
    
    path('locations/suburbs/', LocationViewSet.as_view({'get': 'suburbs', 'post': 'create_suburb'}), name='suburb-list'),
    path('locations/suburbs/<int:pk>/', LocationViewSet.as_view({'get': 'suburb_detail', 'put': 'suburb_detail', 'patch': 'suburb_detail', 'delete': 'suburb_detail'}), name='suburb-detail'),
    
    path('locations/location-hierarchy/', LocationViewSet.as_view({'get': 'location_hierarchy'}), name='location-hierarchy'),
    path('', include(router.urls)),
]