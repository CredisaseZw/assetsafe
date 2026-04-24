from django.apps import AppConfig
from django.contrib.admin import sites
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    verbose_name = _("User Management")

    def ready(self):
        sites.AdminSite.site_header = _("Assetsafe Administration")
        sites.AdminSite.site_title = _("Assetsafe  Admin Portal")
        sites.AdminSite.index_title = _("Welcome to Assetsafe Admin")
