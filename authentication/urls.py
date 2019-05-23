from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserListViewSet, UserDetailViewSet

router = routers.DefaultRouter()
router.register(r"users", UserListViewSet)
router.register(r"user", UserDetailViewSet)

app_name = "authentication"
urlpatterns = [
    path("", include(router.urls)),
    path("login/", obtain_jwt_token, name="login"),
]
