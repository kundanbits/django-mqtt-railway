from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Accelerometer
import json


# Home page (Graph page)
def home(request):
    return render(request, "pages/home.html")


# API to fetch sensor data
def sensor_data(request):
    last_id = request.GET.get("last_id")

    if last_id:
        # Fetch only new records
        data = Accelerometer.objects.filter(id__gt=last_id).order_by("id")
    else:
        # First load ? latest 50 records in correct ascending order
        data = Accelerometer.objects.order_by("-id")[:50]
        data = data.order_by("id")

    data = list(data.values("x", "y", "z", "id"))
    return JsonResponse(data, safe=False)


# API to save sensor data (POST)
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
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=400
            )

    return JsonResponse(
        {"status": "error", "message": "Invalid request"},
        status=400
    )