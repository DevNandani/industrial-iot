
from django.db import models


class Machine(models.Model):
    STATUS_CHOICES = [
        ("RUNNING", "Running"),
        ("STOPPED", "Stopped"),
        ("MAINTENANCE", "Under Maintenance"),
    ]

    machine_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    temperature = models.FloatField(default=0.0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="STOPPED",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def health_status(self):
        if self.temperature >= 70:
            return "CRITICAL"
        elif self.temperature >= 60:
            return "WARNING"
        return "NORMAL"

    def __str__(self):
        return f"{self.machine_id} - {self.name}"


class TemperatureLog(models.Model):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="temperature_logs",
    )
    temperature = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.machine.machine_id} - {self.temperature} °C"
