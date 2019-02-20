from django.urls import path, include
from rest_framework import routers
from .views import UserListViewSet

router = routers.DefaultRouter()
router.register(r'^users', UserListViewSet, basename='users')

app_name = 'authentication'
urlpatterns = [
    path('', include(router.urls)),
]