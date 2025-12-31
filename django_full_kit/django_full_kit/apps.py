from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class FullKitConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_full_kit"
    verbose_name = _("full models")