from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from servers.models import DeviceAlarm
from servers.tasks import check_alarm
from datetime import datetime, timedelta
import django_rq


@receiver(post_save, sender=DeviceAlarm)
def create_scheduler(sender, instance, created, **kwargs):

    new_job_kwargs = {"device_alarm_id": instance.id}
    scheduler = django_rq.get_scheduler('default')
    jobs = [i for i in scheduler.get_jobs() if i.kwargs == new_job_kwargs]
    if jobs:
        scheduler.cancel(jobs[0])
    scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=check_alarm,
        args=None,
        kwargs=new_job_kwargs,
        interval=instance.frequency,
        repeat=None,
        meta={}
    )


@receiver(pre_delete, sender=DeviceAlarm)
def delete_scheduler(sender, instance, **kwargs):

    scheduler = django_rq.get_scheduler('default')
    old_job_kwargs = {"device_alarm_id": instance.id}
    jobs = [i for i in scheduler.get_jobs() if i.kwargs == old_job_kwargs]
    if jobs:
        scheduler.cancel(jobs[0])
