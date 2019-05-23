import jwt
import os
import re
from rest_framework import serializers


def decode_token(token):

    """It handles token decode

    :param token: jwt token value
    :return: decoded jwt token
    """
    return jwt.decode(token, os.environ.get("SECRET_KEY"))


def password_validate(password):
    """It validates password using regular expression

    :param password: contains the users password
    :returns: Boolean
    :raises: ValidationError
    """

    if re.match(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        password,
    ):
        return True
    raise serializers.ValidationError(
        {
            "message": "Password must be at least 8 characters long, at least one"
            + " capitalized character, alphanumeric and contain special characters."
        }
    )


def email_validate(email=None):
    """It validates email using regular expression

    :param email: users email
    :returns: email
    :raises: ValidationError
    """
    if email:
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return email
        raise serializers.ValidationError({"email": "Enter a valid email address."})
