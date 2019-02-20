from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserListViewSet

router = routers.DefaultRouter()
router.register(r'^users', UserListViewSet, basename='users')

app_name = 'authentication'
urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_jwt_token),
]