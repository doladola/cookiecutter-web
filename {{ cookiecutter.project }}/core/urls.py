from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("partials/server-time/", views.server_time, name="server_time"),
]
