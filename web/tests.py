from django.test import TestCase


class ApplicationTests(TestCase):

    def test_home_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CI/CD Pipeline Demonstration")
        self.assertContains(response, "Samuel Mwangangi")
        self.assertContains(response, "Jenkins")
        self.assertContains(response, "Ansible")

    def test_health_endpoint(self):
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "status": "healthy",
            "application": "jenkins-django-demo"
        })
