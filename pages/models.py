from django.db import models

class Accelerometer(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"
