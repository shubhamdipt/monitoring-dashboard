from django.contrib.admin import AdminSite
from servers.models import Device


class CustomAdminSite(AdminSite):

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        # do whatever you want to do and save the values in `extra_context`
        devices = Device.objects.all()
        extra_context['devices'] = devices
        extra_context['devices_count'] = devices.count()

        return super(CustomAdminSite, self).index(request, extra_context)


custom_admin_site = CustomAdminSite()