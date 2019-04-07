from rest_framework import viewsets
from rest_framework.decorators import action
from datetime import datetime, timezone
from django.db import IntegrityError
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from flight.models import Flight
from .models import Book
from .serializers import BookSerializer



class BookListViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API viewset that allows users book flight
    """

    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            try:
                flight_id = serializer.validated_data['flight_id']
                flight = get_object_or_404(Flight, pk=flight_id)
                if flight and flight.is_available:
                    flight.number_booked += 1
                    serializer.save(user=self.request.user)
                    flight.save()
                    return Response({
                        'status': 'Success', 'flights': serializer.data
                    }, status=HTTP_200_OK)
                return Response({
                    'status': 'Failure', 'message': 'Flight is fully booked or not available'
                }, status=HTTP_400_BAD_REQUEST)
            except IntegrityError:
                return Response({
                    'status': 'Failure',
                    'message': 'You cannot book the same flight again'
                    }, status=HTTP_409_CONFLICT)
        return Response({ 'messages': serializer.errors }, status=HTTP_400_BAD_REQUEST)