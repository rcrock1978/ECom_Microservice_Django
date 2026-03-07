from django.apps import AppConfig


class AuthServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'services.auth_service.auth_service'
    label = 'auth_service'
