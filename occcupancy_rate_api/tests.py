from django.test import TestCase
from django.urls import reverse

class MyApiTest(TestCase):
    def test_api_response(self):
        response = self.client.get(reverse('occcupancy_rate_api'))
        self.assertEqual(response.status_code, 200)
