from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sensor-data/', views.sensor_data, name='sensor_data'),
    path('api/sensor/', views.save_sensor_data, name='save_sensor_data'),
]