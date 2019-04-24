from django.db import models
from django.utils.translation import ugettext_lazy as _


class Device(models.Model):
    """Model for the devices"""

    name = models.CharField(_("Name"), max_length=256, unique=True)
    ip_address = models.GenericIPAddressField(_("IP Address"), unique=True)
    created = models.DateTimeField(_("Created At"), auto_now_add=True)
    active = models.BooleanField(_("Active"), default=True)
    notes = models.TextField(_("Notes"), null=True, blank=True)

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")

    def __str__(self):
        return self.name


class DeviceData(models.Model):
    """Data from a certain device"""

    DATA_TYPES = {
        "CPU_USAGE": 0,
        "MEMORY_USAGE": 1,
        "DISK_SPACE_LEFT": 2
    }

    DATA_TYPE_CHOICES = ((val, _(key)) for key, val in DATA_TYPES.items())

    device = models.ForeignKey(
        Device,
        verbose_name=_("Device"),
        on_delete=models.CASCADE,
    )
    data_type = models.IntegerField(
        _("Data Type"),
        choices=DATA_TYPE_CHOICES
    )
    data = models.IntegerField(_("Value"), default=0)
    created = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Device Data")
        verbose_name_plural = _("Device Data")

    def __str__(self):
        return str(self.pk)