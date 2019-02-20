from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    """A serializer for Admin profile object with jwt rendered"""
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name','username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6},
            'username': {'min_length': 2},
        }

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()    
        return user