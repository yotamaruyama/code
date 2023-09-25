# models.py

from django.db import models

class MachineData(models.Model):
    timestamp = models.DateTimeField()
    is_operational = models.BooleanField(default=False)
