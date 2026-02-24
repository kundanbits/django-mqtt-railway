from django.urls import path
from . import views

# urls.py

urlpatterns = [
    # Homepage now shows temperature
    path('', views.temperature_page),

    # Web Page paths
    path('temperature/', views.temperature_page, name='temp_monitor'),
    path('accelerometer/', views.accelerometer_page),

    # API Endpoints (Keep these the same for your ESP8266)
    path('microphone-data/', views.microphone_data),   # JS in temp.html calls this
    path('api/microphone/', views.save_microphone_data), # ESP8266 posts here
    
    path('sensor-data/', views.sensor_data),
    path('api/sensor/', views.save_sensor_data),
]
