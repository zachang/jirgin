from django.urls import path, include
from rest_framework import routers
from .views import FlightListViewSet

router = routers.DefaultRouter()
router.register(r'^flights', FlightListViewSet, basename='flights')

app_name = 'flight'
urlpatterns = [
    path('', include(router.urls)),
]