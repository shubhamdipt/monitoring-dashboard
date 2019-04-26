from django.db import models
from django.utils.translation import ugettext_lazy as _
from notifications.models import Notification


DATA_TYPES = {
    "CPU_USAGE": 0,
    "MEMORY_USAGE": 1,
    "DISK_SPACE_LEFT": 2
}
DATA_TYPE_CHOICES = ((val, _(key)) for key, val in DATA_TYPES.items())


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


class Alarm(models.Model):
    """Model for alarms"""

    COMPARISON = (
        (0, "="),
        (1, ">"),
        (2, "<")
    )
    data_type = models.IntegerField(
        _("Data Type"),
        choices=DATA_TYPE_CHOICES
    )
    comparison_type = models.IntegerField("Comparison", choices=COMPARISON)
    comparison_value = models.FloatField("Value", help_text="Either in % or in GB")

    class Meta:
        verbose_name = _("Alarm")
        verbose_name_plural = _("Alarms")

    def __str__(self):
        return "{} {} {}".format(
            self.get_data_type_display(),
            self.get_comparison_type_display(),
            self.comparison_value
        )


class DeviceAlarm(models.Model):
    """Model for device alarms"""

    device = models.ForeignKey(
        Device,
        verbose_name=_("Device"),
        on_delete=models.CASCADE,
    )
    alarm = models.ForeignKey(
        Alarm,
        verbose_name=_("Alarm"),
        on_delete=models.CASCADE,
    )
    notification = models.ForeignKey(
        Notification,
        verbose_name=_("Notification"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    last_reported = models.DateTimeField(_("Last reported"), null=True, blank=True)
    created = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Device Alarm")
        verbose_name_plural = _("Device Alarms")

    def __str__(self):
        return "{}: {}".format(self.device, self.alarm)
