# pages/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/sensor/', views.save_sensor_data, name='save_sensor_data'),  # <-- Make sure this is included
    path('sensor-data/', views.sensor_data, name='sensor_data'),
]
