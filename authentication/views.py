from copy import deepcopy
from django.contrib.admin.utils import lookup_field
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.parsers import JSONParser
from cloudinary.uploader import upload

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    UserSerializer,
    UserModifySerializer,
    ChangePasswordSerializer,
    ImageSerializer,
)
from .helpers import decode_token, password_validate
from .models import UserProfile


@api_view(["GET"])
def home(request):
    return Response({"message": "Welcome to jirgin, your one stop flight booking app"})


class UserListViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """
    API viewset that allows users to create and view profile
    """

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

    def list(self, request, format=None):
        """It returns all registered users

        :param request: request data
        :param format: format of request
        :returns: response message
        """
        serializer = self.get_serializer(self.queryset, many=True)
        serializer_data = deepcopy(serializer.data)
        for data in serializer_data:
            data["image"] = (
                data["userprofile"]["image"] if data["userprofile"]["image"] else ""
            )
            del data["userprofile"]
        return Response({"users": serializer_data}, status=HTTP_200_OK)


class UserDetailViewSet(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    API viewset that allows users to retrieve, update and delete their own data
    """

    queryset = User.objects.all().order_by("-date_joined")
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserModifySerializer

    lookup_field = "pk"

    @action(detail=False, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        """It handles change password for users

        :param request: request data
        :param pk: primary key
        :returns: response message
        """

        user_id = decode_token(request.auth)["user_id"]
        user = User.objects.get(pk=user_id)
        data = JSONParser().parse(request)
        serializer = ChangePasswordSerializer(data=data)

        if serializer.is_valid():

            old_pass = serializer.data["old_pass"]
            new_pass = serializer.data["new_pass"]
            confirm_new_pass = serializer.data["confirm_new_pass"]

            if old_pass == new_pass:
                return Response(
                    {"message": "Old and new password cannot be the same"},
                    status=HTTP_400_BAD_REQUEST,
                )

            if new_pass != confirm_new_pass:
                return Response(
                    {"message": "New and cofirm password should be the same"},
                    status=HTTP_400_BAD_REQUEST,
                )

            if check_password(old_pass, user.password):
                if password_validate(new_pass):
                    user.password = make_password(new_pass)
                    user.save()
                    return Response(
                        {"message": "Password changed successfully"}, status=HTTP_200_OK
                    )
            else:
                return Response(
                    {"message": "Old Password is not correct"},
                    status=HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def upload_image(self, request, pk=None):
        """It handles image upload to cloudinary

        :param request: request data
        :param pk: primary key
        :returns: response message
        """

        user_id = decode_token(request.auth)["user_id"]
        user = UserProfile.objects.get(user_id=user_id)
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_image = upload(request.data["image"])
            user.image = uploaded_image["secure_url"]
            user.save()
            return Response({"image": uploaded_image["secure_url"]}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
