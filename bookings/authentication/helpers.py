import jwt
import os
import re
from rest_framework import serializers

def decode_token(token):
    return jwt.decode(token, os.environ.get('SECRET_KEY'))


def password_validate(password):
    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        password):
        return True
    raise serializers.ValidationError({
        'password': 'Password must be at least 8 characters long, alphanumeric and contain' + 
        ' special characters.'
    })