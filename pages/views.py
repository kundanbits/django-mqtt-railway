from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Accelerometer, Microphone
import json


# ===================== PAGES =====================

def accelerometer_page(request):
    return render(request, "pages/home.html")


def microphone_page(request):
    return render(request, "pages/microphone.html")


# ===================== ACCELEROMETER =====================

def sensor_data(request):
    last_id = request.GET.get("last_id", 0)

    try:
        last_id = int(last_id)
    except:
        last_id = 0

    if last_id > 0:
        data = Accelerometer.objects.filter(id__gt=last_id) \
                                     .order_by("id") \
                                     .values("x", "y", "z", "id")
        data = list(data)
    else:
        data = Accelerometer.objects.order_by("-id") \
                                    .values("x", "y", "z", "id")[:50]
        data = list(reversed(data))

    return JsonResponse(data, safe=False)


@csrf_exempt
def save_sensor_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            x = float(data.get("x", 0))
            y = float(data.get("y", 0))
            z = float(data.get("z", 0))

            Accelerometer.objects.create(x=x, y=y, z=z)

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


# ===================== MICROPHONE =====================

def microphone_data(request):
    last_id = request.GET.get("last_id", 0)

    try:
        last_id = int(last_id)
    except:
        last_id = 0

    if last_id > 0:
        data = Microphone.objects.filter(id__gt=last_id) \
                                 .order_by("id") \
                                 .values("level", "id")
        data = list(data)
    else:
        data = Microphone.objects.order_by("-id") \
                                 .values("level", "id")[:50]
        data = list(reversed(data))

    return JsonResponse(data, safe=False)


@csrf_exempt
def save_microphone_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            level = float(data.get("level", 0))

            Microphone.objects.create(level=level)

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)