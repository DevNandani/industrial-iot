from rest_framework import serializers
from .models import Machine, TemperatureLog


class MachineSerializer(serializers.ModelSerializer):
    health_status = serializers.ReadOnlyField()

    class Meta:
        model = Machine
        fields = [
            "id",
            "machine_id",
            "name",
            "location",
            "temperature",
            "status",
            "health_status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_machine_id(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Machine ID cannot be empty."
            )
        return value

    def validate_temperature(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Temperature cannot be negative."
            )
        if value > 200:
            raise serializers.ValidationError(
                "Temperature cannot exceed 200°C."
            )
        return value


class TemperatureLogSerializer(serializers.ModelSerializer):
    machine_id = serializers.CharField(
        source="machine.machine_id",
        read_only=True,
    )

    class Meta:
        model = TemperatureLog
        fields = [
            "id",
            "machine_id",
            "temperature",
            "recorded_at",
        ]
        read_only_fields = fields
