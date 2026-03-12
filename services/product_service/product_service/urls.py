from django.urls import path, include

urlpatterns = [
    path('', include('services.product_service.catalog.presentation.urls')),
]
