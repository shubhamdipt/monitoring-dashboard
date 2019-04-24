from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from servers.models import DeviceData, Device


@require_POST
@csrf_exempt
def add_server_data(request):
    try:
        device_ip = request.POST.get("DEVICE_IP")
        device = Device.objects.get(
            ip_address=device_ip
        )
        for key in DeviceData.DATA_TYPES.keys():
            if key in request.POST:
                DeviceData.objects.create(
                    device=device,
                    data_type=DeviceData.DATA_TYPES[key],
                    data=request.POST.get(key)
                )
    except Exception as e:
        print(e)
        return JsonResponse({"status": "ERROR"})
    return JsonResponse({"status": "OK"})