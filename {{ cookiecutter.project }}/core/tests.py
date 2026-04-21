from django.core.management import call_command
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from .demo import get_starter_snapshot, run_celery_probe
from .models import ServiceProbe


class CoreViewsTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django starter is ready")
        self.assertContains(response, "Starter services")

    def test_server_time_partial(self):
        response = self.client.get(reverse("server_time"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Server time")

    def test_service_status_partial(self):
        response = self.client.get(reverse("service_status"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PostgreSQL ready")
        self.assertContains(response, "Redis ready")


class StarterDemoTests(TestCase):
    def test_starter_snapshot_creates_probe_and_round_trips_redis(self):
        snapshot = get_starter_snapshot()

        self.assertTrue(snapshot.redis_ok)
        self.assertEqual(ServiceProbe.objects.filter(slug="starter-demo").count(), 1)
        self.assertGreaterEqual(snapshot.probe_count, 1)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
    def test_celery_probe_runs_in_eager_mode(self):
        self.assertEqual(run_celery_probe(timeout=1), "pong")

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
    def test_verify_stack_command(self):
        call_command("verify_stack", timeout=1)
