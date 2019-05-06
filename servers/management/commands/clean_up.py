from django.core.management.base import BaseCommand
from servers.models import DeviceData
from datetime import datetime, timedelta
from django.utils import timezone
import sys
import time


class Command(BaseCommand):
    help = "Clean up past data"

    def add_arguments(self, parser):
        parser.add_argument(
            'days',
            type=int,
            help='Indicates the number of past days data to be kept.')

    def handle(self, *args, **kwargs):
        days = kwargs['days']
        try:
            while True:
                DeviceData.objects.filter(created__lt=timezone.now() - timedelta(days=days)).delete()
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            print("Interrupted.")
            sys.exit(1)  # break or raise

