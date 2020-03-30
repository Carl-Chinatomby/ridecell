from django.test import TestCase
from api.v1.scooters.models import Scooter


class ScooterTestCase(TestCase):
    fixtures = ['scooters.json']

    def test_get_scooter_by_id(self):
        scooter = Scooter.get_scooter_by_id(1)
        self.assertIsNotNone(scooter)

    def test_get_available_scooters_by_radius(self):
        scooters = Scooter.get_available_scooters_by_radius(
            latitude=1,
            longitude=1,
            radius=20,
        )
        self.assertEqual(len(scooters), 1)

        scooters = scooters = Scooter.get_available_scooters_by_radius(
            latitude=21,
            longitude=21,
            radius=20,
        )
        self.assertEqual(len(scooters), 0)


    def test_reserve(self):
        scooter = Scooter.get_scooter_by_id(1)
        scooter.reserve()
        self.assertTrue(scooter.is_reserved)

    def test_end_reservation(self):
        scooter = Scooter.get_scooter_by_id(1)
        scooter.reserve()
        self.assertTrue(scooter.is_reserved)
        scooter.end_reservation()
        self.assertFalse(scooter.is_reserved)
