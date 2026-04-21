from django.shortcuts import render
from django.utils import timezone

from .demo import get_starter_snapshot


def home(request):
    return render(request, "core/home.html", {"now": timezone.now()})


def server_time(request):
    return render(request, "core/partials/server_time.html", {"now": timezone.now()})


def service_status(request):
    return render(request, "core/partials/service_status.html", {"snapshot": get_starter_snapshot()})
