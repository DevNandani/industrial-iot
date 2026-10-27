
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Machine, TemperatureLog


# ==========================================
# 1. MACHINE HEALTH TESTS
# ==========================================

class MachineHealthTest(TestCase):

    def test_normal_temperature(self):
        machine = Machine(
            machine_id="T001",
            name="Test Motor",
            location="Factory 1",
            temperature=55,
        )
        self.assertEqual(machine.health_status, "NORMAL")

    def test_warning_temperature(self):
        machine = Machine(
            machine_id="T002",
            name="Test Motor",
            location="Factory 1",
            temperature=65,
        )
        self.assertEqual(machine.health_status, "WARNING")

    def test_critical_temperature(self):
        machine = Machine(
            machine_id="T003",
            name="Test Motor",
            location="Factory 1",
            temperature=75,
        )
        self.assertEqual(machine.health_status, "CRITICAL")


# ==========================================
# 2. MACHINE API TESTS
# ==========================================

class MachineAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_machine_list(self):
        response = self.client.get("/api/machines/")
        self.assertEqual(response.status_code, 200)

    def test_create_machine(self):
        data = {
            "machine_id": "TEST001",
            "name": "Test Motor",
            "location": "Factory 1",
            "temperature": 50,
            "status": "RUNNING",
        }

        response = self.client.post(
            "/api/machines/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 201)

    def test_reject_negative_temperature(self):
        data = {
            "machine_id": "TEST002",
            "name": "Test Motor",
            "location": "Factory 1",
            "temperature": -5,
            "status": "RUNNING",
        }

        response = self.client.post(
            "/api/machines/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_reject_temperature_above_200(self):
        data = {
            "machine_id": "TEST003",
            "name": "Test Motor",
            "location": "Factory 1",
            "temperature": 201,
            "status": "RUNNING",
        }

        response = self.client.post(
            "/api/machines/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_reject_invalid_status(self):
        data = {
            "machine_id": "TEST004",
            "name": "Test Motor",
            "location": "Factory 1",
            "temperature": 50,
            "status": "BROKEN",
        }

        response = self.client.post(
            "/api/machines/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_unknown_machine_returns_404(self):
        response = self.client.get(
            "/api/machines/DOES_NOT_EXIST/"
        )

        self.assertEqual(response.status_code, 404)


# ==========================================
# 3. AUTOMATIC TEMPERATURE LOGGING TESTS
# ==========================================

class TemperatureLoggingTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_machine_creates_temperature_log(self):
        response = self.client.post(
            "/api/machines/",
            {
                "machine_id": "LOG001",
                "name": "Logging Test Motor",
                "location": "Factory 1",
                "temperature": 45,
                "status": "RUNNING",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        machine = Machine.objects.get(
            machine_id="LOG001"
        )

        self.assertEqual(
            machine.temperature_logs.count(),
            1,
        )

        log = machine.temperature_logs.first()
        self.assertEqual(log.temperature, 45)

    def test_temperature_change_creates_log(self):
        machine = Machine.objects.create(
            machine_id="LOG002",
            name="Temperature Update Motor",
            location="Factory 1",
            temperature=45,
            status="RUNNING",
        )

        initial_log_count = (
            machine.temperature_logs.count()
        )

        response = self.client.patch(
            "/api/machines/LOG002/",
            {"temperature": 85},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        machine.refresh_from_db()

        self.assertEqual(machine.temperature, 85)

        self.assertEqual(
            machine.temperature_logs.count(),
            initial_log_count + 1,
        )

        latest_log = (
            machine.temperature_logs
            .order_by("-recorded_at")
            .first()
        )

        self.assertEqual(latest_log.temperature, 85)

    def test_unchanged_temperature_does_not_create_log(self):
        machine = Machine.objects.create(
            machine_id="LOG003",
            name="Unchanged Temperature Motor",
            location="Factory 1",
            temperature=45,
            status="RUNNING",
        )

        initial_log_count = (
            machine.temperature_logs.count()
        )

        response = self.client.patch(
            "/api/machines/LOG003/",
            {"temperature": 45},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        machine.refresh_from_db()

        self.assertEqual(
            machine.temperature_logs.count(),
            initial_log_count,
        )
