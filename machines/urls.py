from django.urls import path
from . import views

app_name = "machines"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path(
        "machines/<str:machine_id>/",
        views.machine_detail_page,
        name="machine-detail-page",
    ),

    path("api/machines/", views.machine_list_api, name="machine-list-api"),

    path(
        "api/machines/<str:machine_id>/",
        views.machine_detail_api,
        name="machine-detail-api",
    ),

    path(
        "api/machines/<str:machine_id>/temperature-history/",
        views.machine_temperature_history_api,
        name="machine-temperature-history-api",
    ),

    path("api/alerts/", views.machine_alerts_api, name="machine-alerts-api"),
]
