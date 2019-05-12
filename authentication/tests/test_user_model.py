from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from rest_framework.reverse import reverse

from ..models import UserProfile


class UserModelTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""

        self.user_1 = User.objects.create_user(
            first_name="John",
            last_name="Kenedy",
            username="johnny",
            password="Phrase908",
            email="johnny@gmail.com",
        )
        self.user_2 = User.objects.create_user(
            first_name="Kent",
            last_name="Philip",
            username="kenty",
            password="Phrase908",
            email="kent@gmail.com",
        )

    def test_user_creation_is_successful(self):
        """Test the user created exist in the user model."""
        user_1 = User.objects.get(pk=self.user_1.id)
        user_2 = User.objects.get(pk=self.user_2.id)
        user_count = User.objects.count()

        self.assertEqual(user_1.first_name, "John")
        self.assertEqual(user_2.first_name, "Kent")
        self.assertEqual(user_count, 2)

    def test_user_profile_creation_is_successful(self):
        """Test related user profile model also contains user data."""
        user_profile = UserProfile.objects.get(user_id=self.user_1.id)
        user_profile_count = UserProfile.objects.count()
        self.assertEqual(user_profile_count, 2)
        self.assertEqual(
            str(user_profile), "{}'s profile".format(user_profile.user.username)
        )
