from rest_framework import serializers
from datetime import datetime, timezone
from .models import Flight


class FlightSerializer(serializers.ModelSerializer):
    """A serializer for Flight object"""

    class Meta:
        model = Flight
        fields = ("departure", "arrival", "fly_from", "fly_to", "capacity")

        extra_kwargs = {
            "fly_from": {"min_length": 2, "max_length": 100, "allow_blank": False},
            "fly_to": {"min_length": 2, "max_length": 100, "allow_blank": False},
            "capacity": {"required": True, "min_value": 10},
        }
