from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class BaseModel(models.Model):
    """
    An abstract base model that provides common fields and methods for all models.
    """
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-date_created']
        verbose_name = _("base model")
        verbose_name_plural = _("base models")

    def __str__(self):
        return f"{self.__class__.__name__} (ID: {self.id})"

class BaseModelWithUser(BaseModel):
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT,
                        related_name="%(class)s_created", blank=True, null=True)
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT,
                        related_name="%(class)s_updated", blank=True, null=True)

    class Meta:
        abstract = True