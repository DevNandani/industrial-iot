import random
import time

from django.core.management.base import BaseCommand
from django.db import transaction
from machines.models import Machine, TemperatureLog


class Command(BaseCommand):
    help = "Simulate machine temperatures and record history"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Industrial IoT Sensor Simulator Started!")
        )
        self.stdout.write("Temperature history recording enabled.")
        self.stdout.write("Press Ctrl+C to stop.\n")

        try:
            while True:
                machines = Machine.objects.all()

                if not machines.exists():
                    self.stdout.write(
                        self.style.WARNING(
                            "No machines found. Add machines in Django Admin."
                        )
                    )
                    time.sleep(5)
                    continue

                for machine in machines:
                    change = random.uniform(-2.0, 2.0)
                    temperature = round(
                        max(20.0, min(100.0, machine.temperature + change)),
                        1,
                    )

                    with transaction.atomic():
                        machine.temperature = temperature
                        machine.save(
                            update_fields=["temperature", "updated_at"]
                        )

                        log = TemperatureLog.objects.create(
                            machine=machine,
                            temperature=temperature,
                        )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Machine: {machine.machine_id} | "
                            f"Name: {machine.name} | "
                            f"Temperature: {temperature} °C | "
                            f"Health: {machine.health_status} | "
                            f"Log ID: {log.pk}"
                        )
                    )

                self.stdout.write("-" * 60)
                time.sleep(5)

        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING("\nSensor simulator stopped.")
            )
