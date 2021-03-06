from django.contrib import admin
from servers.models import (
    Device,
    DeviceData,
    Alarm,
    DeviceAlarm,
    DATA_TYPES,
)
from servers.forms import AlarmForm


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "ip_address", "created", "active", )
    ordering = ("-created",)
    list_filter = ("active", )


@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):

    list_display = ("id", "device", "data_type", "readable_value", "created", )
    list_filter = ("device", "data_type", )
    ordering = ("-created", )
    readonly_fields = ("device", "data_type", "data", )


@admin.register(DeviceAlarm)
class DeviceAlarmAdmin(admin.ModelAdmin):

    list_display = ("id", "device", "alarm", "frequency", "notification", "last_reported", )
    ordering = ("-created",)
    list_filter = ("alarm", "last_reported", "device", )


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):

    form = AlarmForm

    list_display = ("id", "data_type", "comparison_type", "readable_value", )
    list_filter = ("data_type", )
