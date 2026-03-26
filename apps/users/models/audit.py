# common/models/audit_log.py

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.common.models.base_models import BaseModel,BaseModelWithUser

class AuditLog(BaseModelWithUser): 
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255, help_text=_("Description of the action performed."))
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text=_("IP address from which the action originated."))
    user_agent = models.TextField(blank=True, help_text=_("User agent string of the client."))
    details = models.JSONField(null=True, blank=True, help_text=_("Detailed context of the action (e.g., changed fields, old/new values, request data)."))
    resource_type = models.CharField(max_length=100, blank=True, null=True, help_text=_("Type of resource affected (e.g., 'User', 'Company', 'Property')."))
    resource_id = models.PositiveIntegerField(null=True, blank=True, help_text=_("ID of the resource affected."))
    success = models.BooleanField(default=True, help_text=_("Whether the action was successful."))
    
    class Meta:
        verbose_name = _("Audit Log")
        verbose_name_plural = _("Audit Logs")
        ordering = ['-timestamp']

    def __str__(self):
        user_info = self.created_by.username if self.created_by else 'Anonymous'
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {user_info}: {self.action}"