from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

from ..helpers import decode_token, password_validate, email_validate


class ListCreateTestCase(APITestCase):
    """Test for api users creation and retrieval"""

    def setUp(self):
        """Define the test client and other test variables."""

        self.user_1 = User.objects.create_user(
            first_name="Johnny",
            last_name="Kenedy",
            username="johnny1",
            password="Phrase908?",
            email="johnny1@gmail.com",
        )
        self.user_1.is_staff = True
        self.user_1.save()

        self.user_2 = User.objects.create_user(
            first_name="Jain",
            last_name="Clarkson",
            username="jainny",
            password="Phrase908?",
            email="jainny@gmail.com",
        )

        self.user_data = {
            "first_name": "Kingley",
            "last_name": "Dabo",
            "username": "kingsy",
            "password": "Phrase908?",
            "email": "kingsy@gmail.com",
        }

        self.auth_user_data_1 = {"username": "johnny1", "password": "Phrase908?"}
        self.auth_user_data_2 = {"username": "jainny", "password": "Phrase908?"}
        self.client = APIClient()
        self.admin_response = self.client.post(
            reverse("authentication:login"), self.auth_user_data_1, format="json"
        )
        self.response_non_admin = self.client.post(
            reverse("authentication:login"), self.auth_user_data_2, format="json"
        )
        self.admin_token = self.admin_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.admin_token)
        self.url_list = reverse("authentication:user-list")
        self.url_detail = reverse(
            "authentication:user-detail",
            args=(decode_token(self.admin_token)["user_id"],),
        )
        self.change_password_url = reverse("authentication:user-change-password")
        self.upload_image_url = reverse("authentication:user-upload-image")

    def test_create_user_successful(self):
        """Verify that new user objects can be created"""
        response = self.client.post(self.url_list, self.user_data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], self.user_data["first_name"])

    def test_create_user_password_format_invalid_unsuccessful(self):
        """Verify that new user objects cannot be created with invalid password type"""
        user_data = {
            "first_name": "Kingley",
            "last_name": "Dabo",
            "username": "kingsy",
            "password": "Phrase908",
            "email": "kingsy@gmail.com",
        }
        message = (
            "Password must be at least 8 characters long, at least one"
            + " capitalized character, alphanumeric and contain special characters."
        )
        response = self.client.post(self.url_list, user_data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["message"][0]), message)

    def test_unauthenticated_user_retrieve_users_unsuccessful(self):
        """Verify that unauthenticated user cannot retrieve users"""
        client = APIClient()
        response = client.get(self.url_list, format="json")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_non_admin_user_retrieve_users_unsuccessful(self):
        """Verify that non admin user cannot retrieve users"""
        client = APIClient()
        token = self.response_non_admin.data["token"]
        client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        response = client.get(self.url_list, format="json")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_admin_retrieve_users_successful(self):
        """Verify that all users can be retrieved by an admin user"""
        response = self.client.get(self.url_list, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.data["users"][1]["first_name"], self.user_1.first_name
        )
        self.assertEqual(len(response.data["users"]), User.objects.count())

    def test_retrieve_single_user_successful(self):
        """Verify retrieval of a single user"""
        response = self.client.get(self.url_detail, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["first_name"], self.user_1.first_name)

    def test_change_password_with_same_old_password_unsuccessful(self):
        """Verify passwords cannot be changed when new password matches old password"""
        message = "Old and new password cannot be the same"
        password_data = {
            "old_pass": "Phrase908?",
            "new_pass": "Phrase908?",
            "confirm_new_pass": "Phrase908?",
        }
        url = reverse("authentication:user-change-password")
        response = self.client.patch(url, password_data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def test_when_new_password_unequals_confirm_new_pass_unsuccessful(self):
        """Verify password change fails when new password and cofirmation do not match"""
        message = "New and cofirm password should be the same"
        password_data = {
            "old_pass": "Phrase908?",
            "new_pass": "Phrase907?",
            "confirm_new_pass": "Phrase906?",
        }
        url = reverse("authentication:user-change-password")
        response = self.client.patch(url, password_data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def test_change_password_with_invalid_old_password_unsuccessful(self):
        """Verify password change fails when previous or old password is not valid"""
        message = "Old Password is not correct"
        password_data = {
            "old_pass": "Phrase907?",
            "new_pass": "Phrase906?",
            "confirm_new_pass": "Phrase906?",
        }
        url = reverse("authentication:user-change-password")
        response = self.client.patch(url, password_data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def test_change_password_when_field_missing_unsuccessful(self):
        """Verify password change fails when any required field missing"""
        validation_message = "This field is required."
        password_data = {"new_pass": "Phrase906?", "confirm_new_pass": "Phrase906?"}
        url = reverse("authentication:user-change-password")
        response = self.client.patch(url, password_data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["old_pass"][0]), validation_message)

    def test_change_password_successful(self):
        """Verify passwords can be changed successfully"""
        message = "Password changed successfully"
        password_data = {
            "old_pass": "Phrase908?",
            "new_pass": "Phrase907?",
            "confirm_new_pass": "Phrase907?",
        }
        response = self.client.patch(
            self.change_password_url, password_data, format="json"
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["message"], message)

    def test_upload_image_unsuccessful(self):
        """Verify image upload fails when expected image field is missing"""
        message = "No file was submitted."
        image_data = {}
        response = self.client.patch(self.upload_image_url, image_data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["image"][0]), message)

    def test_email_validation_successful(self):
        """Verify email validation works"""
        email = email_validate(email="jainny@gmail.com")
        self.assertTrue(email)
