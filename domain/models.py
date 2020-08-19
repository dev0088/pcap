from django.db import models
from django.utils import timezone

class Domain(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    description = models.TextField(max_length=600, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', 'updated_at')
        unique_together = ('name',)
        # verbose_name = _("Domain")
        # verbose_name_plural = _("Domains")
        managed = True