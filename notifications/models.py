from django.db import models
from django.utils.translation import ugettext_lazy as _


CHANNELS = {
    "Webhook": 0
}


class Notification(models.Model):
    """Model for notifications"""

    NOTIFICATION_CHOICES = ((val, _(key)) for key, val in CHANNELS.items())

    notification_type = models.IntegerField(_("Type"), choices=NOTIFICATION_CHOICES)
    arguments = models.TextField(_("Arguments"), help_text=_("Enter url for webhook."))

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return "{}: {}".format(self.id, self.get_not_type_display())



