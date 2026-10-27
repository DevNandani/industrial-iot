
from django.contrib import admin
from .models import Machine


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = (
        "machine_id",
        "name",
        "location",
        "temperature",
        "status",
    )

    list_filter = ("status",)
    search_fields = ("machine_id", "name", "location")
