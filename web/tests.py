from django.test import TestCase


class ApplicationTests(TestCase):

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jenkins Django Deployment")

    def test_health_endpoint(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")
