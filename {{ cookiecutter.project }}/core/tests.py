from django.test import TestCase
from django.urls import reverse


class CoreViewsTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django starter is ready")

    def test_server_time_partial(self):
        response = self.client.get(reverse("server_time"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Server time")
