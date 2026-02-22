from django.shortcuts import render
from django.http import JsonResponse
from .models import Accelerometer
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, "pages/home.html")

def sensor_data(request):
    last_id = request.GET.get("last_id")

    if last_id:
        data = Accelerometer.objects.filter(id__gt=last_id).order_by('id')
    else:
        # first load
        data = Accelerometer.objects.order_by('id')[:50]

    data = list(data.values('x', 'y', 'z', 'id'))
    return JsonResponse(data, safe=False)

@csrf_exempt
def save_sensor_data(request):
    if request.method == "POST":
        x = float(request.POST.get('x', 0))
        y = float(request.POST.get('y', 0))
        z = float(request.POST.get('z', 0))
        Accelerometer.objects.create(x=x, y=y, z=z)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)