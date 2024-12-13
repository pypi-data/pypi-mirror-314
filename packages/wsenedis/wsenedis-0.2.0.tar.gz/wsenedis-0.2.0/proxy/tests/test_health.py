
from django.test import TestCase
from rest_framework.test import APIClient


class TestHealth(TestCase):

    def test_health(self):
        client = APIClient()
        reponse = client.get('/health/', format='json')
        body = reponse.json()
        self.assertEqual(body, 'ok')

