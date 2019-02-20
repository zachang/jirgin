from django.contrib.admin.utils import lookup_field
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)

from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, UserModifySerializer


@api_view(['GET'])
def home(request):
    return Response({ 
        "message": "Welcome to jirgin, your one stop flight booking app" 
    })

class UserListViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """
    API viewset that allows users to create and view profile
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class UserDetailViewSet(mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
    API viewset that allows users to retrieve, update and delete their own data
    """
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = UserModifySerializer

    lookup_field = 'pk'