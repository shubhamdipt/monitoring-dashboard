from servers.models import DeviceAlarm, DeviceData, DATA_TYPES
from datetime import datetime, timedelta
from django.utils import timezone


def check_alarm(device_alarm_id):
    """Scheduler task for checking an alarm."""

    obj = DeviceAlarm.objects.get(id=device_alarm_id)
    valid_time = timezone.now() - timedelta(seconds=obj.frequency)
    comparison_value = obj.alarm.comparison_value
    if obj.alarm.data_type == DATA_TYPES["DISK_SPACE_LEFT"]:
        comparison_value = int(comparison_value * 1073741824)
    comparison_type = obj.alarm.get_comparison_type_display()
    filter_criteria = {
        "device": obj.device,
        "data_type": obj.alarm.data_type,
        "created__gt": valid_time
    }
    if comparison_type == ">":
        filter_criteria["data__gt"] = comparison_value
    elif comparison_type == "<":
        filter_criteria["data__lt"] = comparison_value

    count = DeviceData.objects.filter(**filter_criteria).count()
    if count > 0 and obj.notification:
        obj.notification.notify(
            "{}: {} ({})".format(obj.alarm.__str__(), obj.device.name, obj.device.ip_address)
        )
        obj.last_reported = timezone.now()
        obj.save()
