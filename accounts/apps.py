from django.apps import AppConfig
from django.conf import settings

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    settings.AUTH_USER_MODEL = "accounts.NewUser"
