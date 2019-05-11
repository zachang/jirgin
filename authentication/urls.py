from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserListViewSet, UserDetailViewSet
from .views import home

router = routers.DefaultRouter()
router.register(r"^users", UserListViewSet, basename="users")
router.register(r"^user", UserDetailViewSet, basename="user")

app_name = "authentication"
urlpatterns = [
    path("home/", home, name="home"),
    path("", include(router.urls)),
    path("login/", obtain_jwt_token),
]
