import re
from rest_framework import serializers
from datetime import datetime
from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_200_OK)


def validate_travel_dates(departure, arrival):
    date_format = '%Y-%m-%dT%H:%M:%SZ'
    status = True
    error_message = ''

    if datetime.strptime(departure, date_format) < datetime.now():
        status = False
        error_message = Response({
            'Message':'Departure time cannot be in the past'
            }, status=HTTP_400_BAD_REQUEST)

    if datetime.strptime(arrival, date_format) < datetime.now():
        status = False
        error_message = Response({
            'Message':'Arrival time cannot be in the past'
            }, status=HTTP_400_BAD_REQUEST)

    if datetime.strptime(departure, date_format) > datetime.strptime(arrival, date_format):
        status = False
        error_message = Response({
            'Message':'Departure time cannot be greater than arrival time'
            }, status=HTTP_400_BAD_REQUEST)

    return status, error_message
