import json

from django.test import (
    Client,
    TestCase,
)
from api.v1.scooters.models import (
    Payments,
    Scooter,
)


class PaymentsTestCase(TestCase):
    fixtures = ['scooters.json']

    def setUp(self):
        self.base_url = '/api/v1/scooters/calc_payment'
        self.pay_url = '/api/v1/scooters/pay'
        self.client = Client()

    def test_simple_calc_payment_works(self):
        data = {
            'distance_traveled': 10.0,
            'payment_rate': 5.0
        }
        resp = self.client.post(self.base_url + '/1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['payment_due'], 50.0)

    def test_simple_pay_works(self):
        data = {
            'id': 1,
            'distance_traveled': 10.0,
            'payment_rate': 5.0
        }

        resp = self.client.post(self.base_url + '/1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['payment_due'], 50.0)

        resp = self.client.post(self.pay_url + '/{}'.format(resp.json()['id']))
        print(resp.json())
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['is_paid'])
