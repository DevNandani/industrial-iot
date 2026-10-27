
import random
import time

from django.core.management.base import BaseCommand
from machines.models import Machine, TemperatureLog


class Command(BaseCommand):
    help = "Simulate machine temperatures and record history"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "Industrial IoT Sensor Simulator Started!"
            )
        )
        self.stdout.write(
            "Temperature history recording enabled."
        )
        self.stdout.write("Press Ctrl+C to stop the simulator.\n")

        try:
            while True:
                machines = Machine.objects.all()

                if not machines.exists():
                    self.stdout.write(
                        self.style.WARNING(
                            "No machines found. Add a machine "
                            "in Django Admin."
                        )
                    )

                for machine in machines:
                    # Generate a small random temperature change
                    change = random.uniform(-2.0, 2.0)

                    # Keep temperature between 20 and 100 degrees
                    new_temperature = max(
                        20.0,
                        min(
                            100.0,
                            machine.temperature + change
                        ),
                    )

                    machine.temperature = round(
                        new_temperature, 1
                    )

                    # Save the latest temperature to the Machine table
                    machine.save(
                        update_fields=[
                            "temperature",
                            "updated_at",
                        ]
                    )

                    # Save this reading to temperature history
                    TemperatureLog.objects.create(
                        machine=machine,
                        temperature=machine.temperature,
                    )

                    # Display the latest reading in the terminal
                    self.stdout.write(
                        f"Machine: {machine.machine_id} | "
                        f"Name: {machine.name} | "
                        f"Temperature: {machine.temperature} °C | "
                        f"Health: {machine.health_status}"
                    )

                self.stdout.write("-" * 60)

                # Wait five seconds before the next reading
                time.sleep(5)

        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING(
                    "\nSensor simulator stopped."
                )
            )
