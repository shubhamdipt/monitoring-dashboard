from django.contrib import admin
from servers.models import Device, DeviceData


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "ip_address", "created", "active", )
    ordering = ("-created",)
    list_filter = ("active", )


@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):

    list_display = ("id", "device", "data_type", "data", "created", )
    list_filter = ("data_type", )
    ordering = ("-created", )
