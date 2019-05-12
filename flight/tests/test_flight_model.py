from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from rest_framework.reverse import reverse

from ..models import Flight


class UserModelTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""

        self.flight_1 = Flight.objects.create(
            departure="2019-05-26 15:00:00+01",
            arrival="2019-05-26 16:00:00+01",
            fly_from="Kaduna",
            fly_to="Lagos",
            capacity=200,
        )

        self.flight_2 = Flight.objects.create(
            departure="2019-05-27 15:00:00+01",
            arrival="2019-05-27 16:00:00+01",
            fly_from="Abuja",
            fly_to="Lagos",
            capacity=200,
        )

    def test_flight_instance_creation_is_successful(self):
        """Test the flights created exist in the flight model."""
        flight_1 = Flight.objects.get(pk=self.flight_1.id)
        flight_2 = Flight.objects.get(pk=self.flight_2.id)
        flight_count = Flight.objects.count()

        self.assertEqual(flight_1.fly_from, "Kaduna")
        self.assertEqual(flight_2.fly_from, "Abuja")
        self.assertEqual(
            str(flight_1),
            "The availability of this flight is {}".format(flight_1.is_available),
        )
        self.assertEqual(flight_count, 2)
