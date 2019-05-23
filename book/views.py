from rest_framework import viewsets
from rest_framework.decorators import action
from datetime import datetime, timezone
from django.db import IntegrityError
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from flight.models import Flight
from .models import Book
from .serializers import BookSerializer
from book.helpers.background_task import BackgroundTaskWorker
from book.helpers.flight_reservation_email import send_flight_reservation_email


class BookListViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API viewset that allows users book flight
    """

    queryset = Book.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """It handles booking of flights

        :param request: request data
        :returns: response message
        """

        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            try:
                flight_id = serializer.validated_data["flight_id"]
                flight = get_object_or_404(Flight, pk=flight_id)
                if flight.number_booked == flight.capacity:
                    flight.is_available = False
                    flight.save()
                    return Response(
                        {"message": "Flight is fully booked"},
                        status=HTTP_400_BAD_REQUEST,
                    )
                if flight and flight.is_available:
                    flight.number_booked += 1
                    serializer.save(user=self.request.user)
                    flight.save()
                    BackgroundTaskWorker.start_work(
                        send_flight_reservation_email,
                        (self.request.user, flight.id, flight.departure),
                    )
                    return Response(
                        {"status": "Success", "booked_flights": serializer.data},
                        status=HTTP_201_CREATED,
                    )
                return Response(
                    {
                        "status": "Failure",
                        "message": "The flight is not available at the moment.",
                    },
                    status=HTTP_400_BAD_REQUEST,
                )
            except IntegrityError:
                return Response(
                    {
                        "status": "Failure",
                        "message": "You cannot book the same flight again",
                    },
                    status=HTTP_409_CONFLICT,
                )
        return Response({"messages": serializer.errors}, status=HTTP_400_BAD_REQUEST)
