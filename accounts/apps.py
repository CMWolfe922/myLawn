from django.apps import AppConfig
from django.conf import settings
class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    
    class Meta:

        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"
        ordering = ["-date_joined", "username", "email"]
