import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Accelerometer


@csrf_exempt
def save_sensor_data(request):
    if request.method == "POST":
        try:
            raw_body = request.body.decode("utf-8")
            print("RAW BODY:", raw_body)

            data = json.loads(raw_body)

            print("PARSED DATA:", data)

            x = float(data.get("x", 0))
            y = float(data.get("y", 0))
            z = float(data.get("z", 0))

            Accelerometer.objects.create(x=x, y=y, z=z)

            return JsonResponse({
                "status": "success",
                "received": data
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Invalid request"
    }, status=400)