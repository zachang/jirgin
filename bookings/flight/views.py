import re

from rest_framework import viewsets
from rest_framework.decorators import action
from datetime import datetime, timezone
from django.db import connection
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .serializers import FlightSerializer
from .models import Flight
from .helpers import validate_travel_dates



class FlightListViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """
    API viewset that allows an admin to create flights and all users to  view available flights
    """

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def list(self, request):
        flights = self.get_queryset()
        serializer = self.get_serializer(flights, many=True)
        if not flights:
            return Response({
                'message': 'Sorry, no available flights for now'
            }, status=HTTP_200_OK)
        return Response({
                'status': 'Success',
                'flights': serializer.data 
            }, status=HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        date_format = '%Y-%m-%dT%H:%M:%SZ'
       
        if serializer.is_valid():
            departure = serializer.validated_data['departure'].strftime(date_format)
            arrival = serializer.validated_data['arrival'].strftime(date_format)
            status, error_message = validate_travel_dates(departure, arrival)

            if status:
                serializer.save()
                return Response({
                    'status': 'Success',
                     'flights': serializer.data
                }, status=HTTP_200_OK)  
            return error_message 
            
        return Response({
                'status': 'Success',
                 'messages': serializer.errors 
            }, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAdminUser])
    def reservations(self, request):
        date = request.query_params.get('date', None)
        if date is None:
            return Response({
                'message': 'please provide a date in the query param.'
                }, status=HTTP_400_BAD_REQUEST)

        if not re.match(r'(^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$)', date):
            return Response(
                {'message': 'Date has wrong format. Use this format YYYY-MM-DD.'},
                status=HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            query = "SELECT number_booked FROM flight_flight WHERE Date(departure)=%s"
            cursor.execute(query,[date])
            count_result = cursor.fetchall()
        if count_result:
            for item in count_result[0]:
                result = item
            return Response({ 'reservations': result }, status=HTTP_200_OK)
        return Response({ 'message': 'this departure date is invalid ' },
            status=HTTP_400_BAD_REQUEST)
