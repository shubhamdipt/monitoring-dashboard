from servers.models import DeviceAlarm, DeviceData, DATA_TYPES
from datetime import datetime, timedelta
from django.utils import timezone
from django_rq import job


def notify(device_alarm_obj, current_value):
    obj = device_alarm_obj
    obj.notification.notify(
        "{}: {} ({})\nValue: {}".format(
            obj.alarm.__str__(),
            obj.device.name,
            obj.device.ip_address,
            current_value
        )
    )
    obj.last_reported = timezone.now()
    obj.save()


@job('high')
def check_alarm(device_alarm_id):
    """Scheduler task for checking an alarm."""

    obj = DeviceAlarm.objects.get(id=device_alarm_id)

    if obj.alarm.data_type == DATA_TYPES["DOWNTIME"]:
        valid_time = timezone.now() - timedelta(
            seconds=int(obj.alarm.comparison_value*60))
        filter_criteria = {
            "device": obj.device,
        }
        device_data = DeviceData.objects.filter(**filter_criteria).latest('created')
        if not device_data:
            notify(obj, "DOWN since {}".format(
                timezone.localtime(valid_time).strftime("%H:%M, %d %B %Y")))
        elif device_data.created < valid_time:
            notify(obj, "DOWN since {}".format(
                timezone.localtime(device_data.created).strftime("%H:%M, %d %B %Y")))
        return

    valid_time = timezone.now() - timedelta(
        seconds=DeviceAlarm.TIME_IN_SECONDS[obj.frequency][0])

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

    device_data = DeviceData.objects.filter(**filter_criteria).order_by("-created")
    if device_data.count() > 0 and obj.notification:
        notify(obj, device_data[0].readable_value)

