from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from .helpers import password_validate, email_validate


class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for user profile object"""

    image = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = ("image",)


class UserSerializer(serializers.ModelSerializer):
    """A serializer for user object"""

    def validate(self, data):
        password = data.get("password", None)
        if password_validate(password):
            return data

    userprofile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
            "email",
            "userprofile",
        )
        extra_kwargs = {
            "username": {
                "min_length": 2,
                "max_length": 30,
                "allow_blank": False,
                "required": True,
            },
            "first_name": {
                "min_length": 2,
                "max_length": 100,
                "allow_blank": False,
                "required": True,
            },
            "last_name": {
                "min_length": 2,
                "max_length": 100,
                "allow_blank": False,
                "required": True,
            },
            "email": {"required": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserModifySerializer(serializers.ModelSerializer):
    """A serializer for updates on user object"""

    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email")
        extra_kwargs = {
            "username": {
                "required": False,
                "min_length": 2,
                "max_length": 30,
                "allow_blank": False,
            },
            "first_name": {
                "required": False,
                "min_length": 2,
                "max_length": 100,
                "allow_blank": False,
            },
            "last_name": {
                "required": False,
                "min_length": 2,
                "max_length": 100,
                "allow_blank": False,
            },
            "email": {"required": False, "allow_blank": False},
        }

    def partial_update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)
        instance.email = email_validate(validated_data.get("email", instance.email))
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """A serializer for password change"""

    old_pass = serializers.CharField(required=True)
    new_pass = serializers.CharField(required=True)
    confirm_new_pass = serializers.CharField(required=True)

    class Meta:
        fields = ("new_pass", "confirm_new_pass", "old_pass")


class ImageSerializer(serializers.ModelSerializer):
    """A serializer for user profile object"""

    image = serializers.ImageField(max_length=None, allow_empty_file=False)

    class Meta:
        model = UserProfile
        fields = ("id", "image")
