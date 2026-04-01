from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.individuals.api.views import IndividualViewSet, BulkUpload
from apps.individuals.utils.templates import download_csv_template, download_excel_template

router = DefaultRouter()
router.register(r'', IndividualViewSet, basename='individual')
router.register(r'bulk-upload', BulkUpload, basename='bulk-upload')

urlpatterns = [
    path('', include(router.urls)),
    path('template/csv/', download_csv_template, name= "csv-template"),
    # path('template/excel/', download_excel_template, name= "xlsx-template"),
    
]