from django.urls import path
from . import views

urlpatterns = [
    path('', views.microphone_page),   # microphone as homepage

    path('microphone/', views.microphone_page),
    path('microphone-data/', views.microphone_data),
    path('api/microphone/', views.save_microphone_data),

    path('accelerometer/', views.accelerometer_page),
    path('sensor-data/', views.sensor_data),
    path('api/sensor/', views.save_sensor_data),
]