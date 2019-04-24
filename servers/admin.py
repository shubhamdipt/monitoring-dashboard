from django.contrib import admin
from servers.models import Device, DeviceData


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "ip_address", "created", "active", )
    ordering = ("-created",)
    list_filter = ("active", )


@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):

    def readable_value(self, obj):
        if obj.data_type == DeviceData.DATA_TYPES["DISK_SPACE_LEFT"]:
            return "{0:.3f} GB".format(float(obj.data / 1073741824))
        return "{} %".format(obj.data)

    list_display = ("id", "device", "data_type", "readable_value", "created", )
    list_filter = ("device", "data_type", )
    ordering = ("-created", )
