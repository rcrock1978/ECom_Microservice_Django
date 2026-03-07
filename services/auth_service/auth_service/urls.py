from django.urls import path
from services.auth_service.presentation import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('password-reset/', views.password_reset),
    path('admin-login/', views.admin_login),
]
