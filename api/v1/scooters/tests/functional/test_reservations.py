import json

from django.test import (
    Client,
    TestCase,
)
from api.v1.scooters.models import Scooter


class ReservationTestCase(TestCase):
    fixtures = ['scooters.json']

    def setUp(self):
        self.base_url = '/api/v1/scooters/reserve'
        self.end_reserve_url = '/api/v1/scooters/end_reservation'
        self.client = Client()

    def test_regular_post_request_works(self):
        resp = self.client.post(self.base_url + '?id=1')
        self.assertEqual(resp.status_code, 200)

    def test_only_post_requests_are_allowed(self):
        resp = self.client.get(self.base_url)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.patch(self.base_url)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.delete(self.base_url)
        self.assertEqual(resp.status_code, 405)

    def test_missing_id_gives_error(self):
        resp = self.client.post(self.base_url)
        self.assertEqual(resp.status_code, 422)

    def test_invalid_non_int_gives_error(self):
        resp = self.client.post(self.base_url + '?id=a')
        self.assertEqual(resp.status_code, 422)

    def test_invalid_non_existant_gives_error(self):
        resp = self.client.post(self.base_url + '?id=10000000')
        self.assertEqual(resp.status_code, 404)

    def test_already_reserved_gives_error(self):
        resp = self.client.post(self.base_url + '?id=1')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(self.base_url + '?id=1')
        self.assertEqual(resp.status_code, 404)

    def test_can_reserve_scooter(self):
        resp = self.client.post(self.base_url + '?id=1')
        self.assertEqual(resp.status_code, 200)

    def test_can_end_reservation_on_scooter(self):
        resp = self.client.post(self.base_url + '?id=1')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(self.end_reserve_url + '?id=1')
        self.assertEqual(resp.status_code, 200)

    def test_cant_end_reservation_on_non_reserved(self):
        resp = self.client.post(self.end_reserve_url + '?id=1')
        self.assertEqual(resp.status_code, 404)
