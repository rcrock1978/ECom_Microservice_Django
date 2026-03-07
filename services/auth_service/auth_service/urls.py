from django.urls import path
from services.auth_service.presentation import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('password-reset/', views.password_reset),
    path('admin-login/', views.admin_login),
    path('refresh/', views.refresh),
    path('logout/', views.logout),
    path('verify/', views.verify_email),
]
