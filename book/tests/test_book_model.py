from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from rest_framework.reverse import reverse

from ..models import Book
from flight.models import Flight


class UserModelTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""

        self.flight = Flight.objects.create(
            departure="2019-05-26 15:00:00+01",
            arrival="2019-05-26 16:00:00+01",
            fly_from="Kaduna",
            fly_to="Lagos",
            capacity=200,
        )

        self.user = User.objects.create_user(
            first_name="Jain",
            last_name="Clarkson",
            username="jainny",
            password="Phrase908?",
            email="jainny@gmail.com",
        )

        self.book = Book.objects.create(
            flight_class="FIRST", user=self.user, flight=self.flight
        )

    def test_book_instance_creation_is_successful(self):
        """Test flight bookings exist in the book model."""
        book = Book.objects.get(pk=self.book.id)
        book_count = Book.objects.count()

        self.assertEqual(book.flight_class, "FIRST")
        self.assertEqual(str(book), "{} class".format(book.flight_class))
        self.assertEqual(book_count, 1)
