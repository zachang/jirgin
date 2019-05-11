from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from rest_framework.reverse import reverse

from . import views


class SanityTestCase(TestCase):
    """Test the sanity of the api and that it can be accessed"""

    def test_welcome_view_successful(self):
        """Test that the api navigates to the home view successful"""
        message = "Welcome to jirgin, your one stop flight booking app"
        self.client = APIClient()
        self.response = self.client.get(reverse("authentication:home"), format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.response.data["message"], message)
