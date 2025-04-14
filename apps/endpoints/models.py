from django.db import models
from django.utils import timezone
from django.conf import settings  # ✅ Use this instead of importing User directly
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        abstract = True

class ApiKey(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)
    key = models.CharField(_("Key"), max_length=255, unique=True, editable=False)
    user = models.ForeignKey(  # ✅ updated
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="api_keys"
    )
    is_active = models.BooleanField(_("Is active"), default=True)
    expires_at = models.DateTimeField(_("Expires at"), null=True, blank=True)
    last_used_at = models.DateTimeField(_("Last used at"), null=True, blank=True)

    class Meta:
        verbose_name = _("API Key")
        verbose_name_plural = _("API Keys")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    def generate_key(self):
        import secrets
        return secrets.token_hex(32)

    @property
    def is_expired(self):
        if self.expires_at is None:
            return False
        return self.expires_at < timezone.now()

    def mark_used(self):
        self.last_used_at = timezone.now()
        self.save(update_fields=["last_used_at"])

class ScheduledTask(TimeStampedModel):
    STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("running", _("Running")),
        ("completed", _("Completed")),
        ("failed", _("Failed")),
        ("cancelled", _("Cancelled")),
    )

    name = models.CharField(_("Task name"), max_length=255)
    task_id = models.CharField(
        _("Celery task ID"), max_length=255, unique=True, null=True, blank=True
    )
    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    scheduled_at = models.DateTimeField(_("Scheduled at"), default=timezone.now)
    started_at = models.DateTimeField(_("Started at"), null=True, blank=True)
    completed_at = models.DateTimeField(_("Completed at"), null=True, blank=True)
    result = models.JSONField(_("Result"), null=True, blank=True)
    error_message = models.TextField(_("Error message"), null=True, blank=True)

    class Meta:
        verbose_name = _("Scheduled Task")
        verbose_name_plural = _("Scheduled Tasks")
        ordering = ["-scheduled_at"]

    def __str__(self):
        return f"{self.name} ({self.status})"
