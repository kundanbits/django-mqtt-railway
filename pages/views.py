from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Accelerometer, Microphone
import json

# ================= PAGES =================

def microphone_page(request):
    """Renders the original microphone/sound dashboard"""
    return render(request, "pages/microphone.html")

def accelerometer_page(request):
    """Renders the accelerometer (home) dashboard"""
    return render(request, "pages/home.html")

def temperature_page(request):
    """Renders the new LM35 Absolute Temperature dashboard"""
    # This matches the /pages/templates/pages/temp.html file you created
    return render(request, "pages/temp.html")

# ... (Keep your existing microphone_data and save_microphone_data views below)


# ================= MICROPHONE =================

def microphone_data(request):
    last_id = request.GET.get("last_id")

    if last_id:
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

            # IMPORTANT: ESP must send {"level": value}
            level = float(data["level"])

            Microphone.objects.create(level=level)

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=400
            )

    return JsonResponse({"status": "error"}, status=400)


# ================= ACCELEROMETER =================

def sensor_data(request):
    last_id = request.GET.get("last_id")

    if last_id:
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

            x = float(data["x"])
            y = float(data["y"])
            z = float(data["z"])

            Accelerometer.objects.create(x=x, y=y, z=z)

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=400
            )

    return JsonResponse({"status": "error"}, status=400)
