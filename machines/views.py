
from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Machine, TemperatureLog
from .serializers import MachineSerializer, TemperatureLogSerializer
from .pagination import MachinePagination


# ==========================================
# 1. MACHINE DASHBOARD
# ==========================================

def dashboard(request):
    machines = list(
        Machine.objects.all().order_by("machine_id")
    )

    critical_machines = [
        m for m in machines if m.temperature >= 70
    ]

    warning_machines = [
        m for m in machines
        if 60 <= m.temperature < 70
    ]

    context = {
        "machines": machines,
        "total_machines": len(machines),

        "running_machines": sum(
            m.status == "RUNNING" for m in machines
        ),
        "stopped_machines": sum(
            m.status == "STOPPED" for m in machines
        ),
        "maintenance_machines": sum(
            m.status == "MAINTENANCE" for m in machines
        ),

        "critical_machines": critical_machines,
        "critical_count": len(critical_machines),

        "warning_machines": warning_machines,
        "warning_count": len(warning_machines),

        "recent_logs": (
            TemperatureLog.objects
            .select_related("machine")
            .order_by("-recorded_at")[:10]
        ),
    }

    return render(
        request,
        "machines/dashboard.html",
        context,
    )


# ==========================================
# 2. MACHINE LIST API
# GET: Retrieve machines with pagination
# POST: Create a machine and log its temperature
# ==========================================

@api_view(["GET", "POST"])
def machine_list_api(request):

    # GET: Retrieve machines with pagination
    if request.method == "GET":
        machines = Machine.objects.all().order_by(
            "machine_id"
        )

        paginator = MachinePagination()

        page = paginator.paginate_queryset(
            machines,
            request,
        )

        serializer = MachineSerializer(
            page,
            many=True,
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    # POST: Create a new machine and log its initial temperature
    serializer = MachineSerializer(
        data=request.data,
    )

    if serializer.is_valid():
        machine = serializer.save()

        TemperatureLog.objects.create(
            machine=machine,
            temperature=machine.temperature,
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


# ==========================================
# 3. INDIVIDUAL MACHINE API
# GET: Retrieve one machine
# PUT: Fully update a machine
# PATCH: Partially update a machine
# DELETE: Delete a machine
# ==========================================

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def machine_detail_api(request, machine_id):

    machine = get_object_or_404(
        Machine,
        machine_id=machine_id,
    )

    # GET: Retrieve one machine
    if request.method == "GET":
        serializer = MachineSerializer(machine)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # PUT: Fully update a machine
    elif request.method == "PUT":
        serializer = MachineSerializer(
            machine,
            data=request.data,
        )

    # PATCH: Partially update a machine
    elif request.method == "PATCH":
        serializer = MachineSerializer(
            machine,
            data=request.data,
            partial=True,
        )

    # Validate and save PUT/PATCH changes
    if request.method in ("PUT", "PATCH"):

        # Store the old temperature before updating
        old_temperature = machine.temperature

        if serializer.is_valid():
            machine = serializer.save()

            # Log only when the temperature has changed
            if machine.temperature != old_temperature:
                TemperatureLog.objects.create(
                    machine=machine,
                    temperature=machine.temperature,
                )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DELETE: Remove a machine
    elif request.method == "DELETE":
        machine.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

# ==========================================
# MACHINE TEMPERATURE HISTORY API
# GET: Retrieve temperature history for one machine
# ==========================================

@api_view(["GET"])
def machine_temperature_history_api(request, machine_id):
    machine = get_object_or_404(
        Machine,
        machine_id=machine_id,
    )

    logs = (
        TemperatureLog.objects
        .filter(machine=machine)
        .order_by("-recorded_at")
    )

    serializer = TemperatureLogSerializer(
        logs,
        many=True,
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


# ==========================================
# TEMPERATURE ALERTS API
# ==========================================

@api_view(["GET"])
def machine_alerts_api(request):
    machines = Machine.objects.filter(
        temperature__gte=60
    ).order_by("-temperature")

    alerts = []

    for machine in machines:
        if machine.temperature >= 70:
            severity = "CRITICAL"
            message = "Critical temperature detected!"
        else:
            severity = "WARNING"
            message = "Temperature is above normal."

        alerts.append({
            "machine_id": machine.machine_id,
            "name": machine.name,
            "temperature": machine.temperature,
            "severity": severity,
            "message": message,
        })

    return Response({
        "count": len(alerts),
        "alerts": alerts,
    })

# ==========================================
# 6. MACHINE DETAIL WEB PAGE
# URL: /machines/M001/
# ==========================================

def machine_detail_page(request, machine_id):
    machine = get_object_or_404(
        Machine,
        machine_id=machine_id,
    )

    temperature_logs = list(
        TemperatureLog.objects
        .filter(machine=machine)
        .order_by("-recorded_at")[:50]
    )

    chart_logs = [
        {
            "recorded_at": log.recorded_at.isoformat(),
            "temperature": log.temperature,
        }
        for log in temperature_logs
    ]

    context = {
        "machine": machine,
        "temperature_logs": temperature_logs,
        "chart_logs": chart_logs,
    }

    return render(
        request,
        "machines/machine_detail.html",
        context,
    )
