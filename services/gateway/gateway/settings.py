import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")
ROOT_URLCONF = "gateway.urls"
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.auth", "rest_framework"]
MIDDLEWARE = []
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
REST_FRAMEWORK = {"DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema"}
SPECTACULAR_SETTINGS = {"TITLE": "Gateway API", "VERSION": "1.0.0"}
