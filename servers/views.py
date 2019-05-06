from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from servers.models import DeviceData, Device, DATA_TYPES
from django.utils import timezone
from datetime import timedelta


@require_POST
@csrf_exempt
def add_server_data(request):
    try:
        device_ip = request.POST.get("DEVICE_IP")
        device = Device.objects.get(
            ip_address=device_ip
        )
        for key in DATA_TYPES.keys():
            if key in request.POST:
                DeviceData.objects.create(
                    device=device,
                    data_type=DATA_TYPES[key],
                    data=request.POST.get(key)
                )
    except Exception as e:
        print(e)
        return JsonResponse({"status": "ERROR"})
    return JsonResponse({"status": "OK"})


@require_POST
@login_required
def plot_server_data(request):
    device_data = dict()
    try:
        device_id = request.POST.get("device_id")
        days = request.POST.get("days")
        now = timezone.now()
        for key, val in DATA_TYPES.items():
            data = list(DeviceData.objects.filter(
                device__id=device_id,
                data_type=val,
                created__gte=(now - timedelta(days=int(days)))
            ).values("created", "data"))
            device_data[key] = data

    except Exception as e:
        print(e)
        return JsonResponse({"status": "ERROR", "data": device_data})
    return JsonResponse({"status": "OK", "data": device_data})