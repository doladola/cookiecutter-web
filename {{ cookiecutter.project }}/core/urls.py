from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("partials/server-time/", views.server_time, name="server_time"),
    path("partials/service-status/", views.service_status, name="service_status"),
]
