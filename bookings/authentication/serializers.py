import re
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

    def validate(self, data):
        password = data.get('password', None)
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            password):
            return data
        raise serializers.ValidationError({
            'password': 'Password must be at least 8 characters long, alphanumeric and contain' + 
            ' special characters.'
        })

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name','username', 'password', 'email')
        extra_kwargs = {
            'username': {
                'min_length': 2, 'max_length': 30, 'allow_blank': False, 'required': True
                },
            'first_name': {
                'min_length': 2, 'max_length': 100, 'allow_blank': False, 'required': True
                },
            'last_name': {
                'min_length': 2, 'max_length': 100, 'allow_blank': False, 'required': True
                }
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

class UserModifySerializer(serializers.ModelSerializer):
    """A serializer for Admin profile object with jwt rendered"""
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name','username', 'email')
        extra_kwargs = {
            'username': {
                'required': False, 'min_length': 2, 
                'max_length': 30, 'allow_blank': False
            },
            'first_name': {
                'required': False, 'min_length': 2,
                'max_length': 100, 'allow_blank': False
            },
            'last_name': {
                'required': False, 'min_length': 2,
                'max_length': 100, 'allow_blank': False
            },
            'email': {'required': False, 'allow_blank': False}
        }

    def partial_update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance



class ChangePasswordSerializer(serializers.Serializer):
    """A serializer for password change"""
    
    old_pass = serializers.CharField(required=True)
    new_pass = serializers.CharField(required=True)
    confirm_new_pass = serializers.CharField(required=True)
    class Meta:
        fields = ('new_pass', 'confirm_new_pass', 'old_pass')