import bookings.settings
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from ..models import Flight
from authentication.helpers import decode_token


class ListCreateTestCase(APITestCase):
    """Test for api users creation and retrieval"""

    def setUp(self):
        """Define the test client and other test variables."""

        self.flight = Flight.objects.create(
            departure="2019-05-26 15:00:00+01",
            arrival="2019-05-26 16:00:00+01",
            fly_from="Kaduna",
            fly_to="Lagos",
            capacity=200,
        )
        self.flight.number_booked = 1
        self.flight.save()

        self.flight_data = dict(
            departure="2019-05-26 10:00:00",
            arrival="2019-05-26 11:00:00",
            fly_from="Kaduna",
            fly_to="Abuja",
            capacity=200,
        )

        self.user_1 = User.objects.create_user(
            first_name="Johnny",
            last_name="Kenedy",
            username="johnny1",
            password="Phrase908?",
            email="johnny1@gmail.com",
        )
        self.user_1.is_staff = True
        self.user_1.save()

        self.auth_user_data_1 = {"username": "johnny1", "password": "Phrase908?"}
        self.client = APIClient()
        self.admin_response = self.client.post(
            reverse("authentication:login"), self.auth_user_data_1, format="json"
        )
        self.admin_token = self.admin_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.admin_token)
        self.url = reverse("flight:flight-list")
        self.reservations_url = reverse("flight:flight-reservations")

    def test_create_flight_successful(self):
        """Verify that new flight objects can be created"""
        response = self.client.post(self.url, self.flight_data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["flights"]["fly_from"], self.flight.fly_from)

    def test_create_flight_with_missing_field_unsuccessful(self):
        """Verify that new flight objects cannot be created with invalid request"""
        flight_data = dict(
            arrival="2019-05-26 11:00:00+01",
            fly_from="Kaduna",
            fly_to="Abuja",
            capacity=200,
        )
        message = "This field is required."
        response = self.client.post(self.url, flight_data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["messages"]["departure"][0], message)

    def test_create_flight_with_elapsed_departure_date_unsuccessful(self):
        """Verify that new flight objects cannot be created with departure date in the past"""
        flight_data = dict(
            departure="2019-05-01 15:00:00+01",
            arrival="2019-05-26 11:00:00+01",
            fly_from="Kaduna",
            fly_to="Abuja",
            capacity=200,
        )
        message = "Departure time cannot be in the past"
        response = self.client.post(self.url, flight_data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def test_create_flight_with_departure_greater_than_arrival_date_unsuccessful(self):
        """
        Verify that new flight objects cannot be created with 
        departure date greater than arrival date
        """
        flight_data = dict(
            departure="2019-05-24 15:00:00+01",
            arrival="2019-05-24 14:00:00+01",
            fly_from="Kaduna",
            fly_to="Abuja",
            capacity=200,
        )
        message = "Departure time cannot be greater than arrival time"
        response = self.client.post(self.url, flight_data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def test_create_flight_with_elapsed_arrival_date_unsuccessful(self):
        """Verify that new flight objects cannot be created with arrival date in the past"""
        flight_data = dict(
            departure="2019-05-24 15:00:00+01",
            arrival="2019-05-01 14:00:00+01",
            fly_from="Kaduna",
            fly_to="Abuja",
            capacity=200,
        )
        message = "Arrival time cannot be in the past"
        response = self.client.post(self.url, flight_data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def test_retrieve_all_created_flights_successful(self):
        """Verify that all created flights can be retrieved"""
        message = "Sorry, no available flights for now"
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["flights"][0]["fly_from"], self.flight.fly_from)

    def test_retrieve_all_flights_when_none_created_successful(self):
        """Verify that fligts can be retrieved though flights might not be created yet"""
        self.flight.delete()
        message = "Sorry, no available flights for now"
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["message"], message)

    def test_retrieve_reservations_any_valid_date_successful(self):
        """Verify all flight reservations for any existing valid date"""
        date = {"date": self.flight_data["departure"].split(" ")[0]}
        response = self.client.get(self.reservations_url, data=date, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["reservations"], self.flight.number_booked)

    def test_retrieve_reservations_for_missing_date_unsuccessful(self):
        """Verify that retrieval of flight reservations fails if no date is supplied"""
        date = {}
        message = "please provide a date in the query param."
        response = self.client.get(self.reservations_url, data=date, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def test_retrieve_reservations_for_invalid_date_format_unsuccessful(self):
        """Verify that retrieval of flight reservations fails if date format is invalid"""
        date = {"date": "12-12-2019"}
        message = "Date has wrong format. Use this format YYYY-MM-DD."
        response = self.client.get(self.reservations_url, data=date, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def test_retrieve_reservations_for_invalid_date_unsuccessful(self):
        """Verify that retrieval of flight reservations fails if date is invalid"""
        date = {"date": "2019-12-12"}
        message = "this departure date is invalid"
        response = self.client.get(self.reservations_url, data=date, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)
