from django.contrib import admin

# Register your models here.

from .models import Accelerometer, Microphone

admin.site.register(Accelerometer)
admin.site.register(Microphone)
