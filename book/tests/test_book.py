from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)

from ..models import Book
from flight.models import Flight


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
            fly_from="Kano",
            fly_to="Lagos",
            capacity=200,
        )

        self.flight_3 = Flight.objects.create(
            departure="2019-05-28 15:00:00+01",
            arrival="2019-05-28 16:00:00+01",
            fly_from="Kano",
            fly_to="Lagos",
            capacity=200,
        )
        self.flight_3.number_booked = 200
        self.flight_3.save()

        self.flight_4 = Flight.objects.create(
            departure="2019-05-29 15:00:00+01",
            arrival="2019-05-29 16:00:00+01",
            fly_from="Kano",
            fly_to="Lagos",
            capacity=200,
        )
        self.flight_4.is_available = False
        self.flight_4.save()

        self.user = User.objects.create_user(
            first_name="Jain",
            last_name="Clarkson",
            username="jainny",
            password="Phrase908?",
            email="jainny@gmail.com",
        )

        self.book = Book.objects.create(
            flight_class="FIRST", user=self.user, flight=self.flight_1
        )

        self.auth_user_data = {"username": "jainny", "password": "Phrase908?"}
        self.client = APIClient()
        self.response = self.client.post(
            reverse("authentication:login"), self.auth_user_data, format="json"
        )
        self.token = self.response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)
        self.book_data = dict(flight_class="FIRST", flight=self.flight_2.id)
        self.url = reverse("book:book-list")

    def test_book_flight_successful(self):
        """Test that flights can be booked successfully."""
        response = self.client.post(self.url, self.book_data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["booked_flights"]["flight_class"], "FIRST")

    def test_book_flight_same_user_same_flight_unsuccessful(self):
        """Test that the same user booking same flight is unsuccessfully."""
        book_data = dict(flight_class="FIRST", flight=self.flight_1.id)
        response = self.client.post(self.url, book_data, format="json")
        message = "You cannot book the same flight again"
        self.assertEqual(response.status_code, HTTP_409_CONFLICT)
        self.assertEqual(response.data["message"], message)

    def test_book_fully_booked_flight_unsuccessful(self):
        """Test that booking a fully booked flight fails."""
        book_data = dict(flight_class="FIRST", flight=self.flight_3.id)
        response = self.client.post(self.url, book_data, format="json")
        message = "Flight is fully booked"
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def test_book_unavailable_flight_unsuccessful(self):
        """Test that booking an unavailable flight fails."""
        book_data = dict(flight_class="FIRST", flight=self.flight_4.id)
        response = self.client.post(self.url, book_data, format="json")
        message = "The flight is not available at the moment."
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def test_book_flight_missing_field_unsuccessful(self):
        """Test that booking with missing field fails."""
        book_data = dict(flight_class="FIRST")
        response = self.client.post(self.url, book_data, format="json")
        message = "This field is required."
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["messages"]["flight"][0]), message)
