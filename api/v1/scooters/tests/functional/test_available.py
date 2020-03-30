import json

from django.test import (
    Client,
    TestCase,
)
from api.v1.scooters.models import Scooter


class AvailableTestCase(TestCase):
    fixtures = ['scooters.json']

    def setUp(self):
        self.base_url = '/api/v1/scooters/available/'
        self.client = Client()

    def test_regular_get_request_works(self):
        resp = self.client.get(self.base_url)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(self.base_url + '?lat=1.0&lon=1.0&radius=20')
        self.assertEqual(len(resp.json()), 1)

    def test_only_get_requests_are_allowed(self):
        resp = self.client.post(self.base_url)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.patch(self.base_url)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.delete(self.base_url)
        self.assertEqual(resp.status_code, 405)

    def test_only_available_scooters_are_returned(self):
        resp = self.client.get(self.base_url + '?lat=1.0&lon=1.0&radius=20')
        self.assertEqual(len(resp.json()), 1)

        scooter = Scooter.get_scooter_by_id(resp.json()[0]['id'])
        self.assertIsNotNone(scooter)
        scooter.reserve()

        resp = self.client.get(self.base_url + '?lat=1.0&lon=1.0&radius=20')
        self.assertEqual(len(resp.json()), 0)

    def test_response_has_correct_fields(self):
        resp = self.client.get(self.base_url + '?lat=1.0&lon=1.0&radius=20')
        fields = list(resp.json()[0].keys())
        self.assertEqual(fields, ['id', 'lat', 'lng'])

    def test_invalid_params(self):
        resp = self.client.get(self.base_url + '?lat=a&lon=1.0&radius=20')
        self.assertEqual(resp.status_code, 422)
