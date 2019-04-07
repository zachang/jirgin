from django.urls import path, include
from rest_framework import routers
from .views import BookListViewSet

router = routers.DefaultRouter()
router.register(r'^books', BookListViewSet, basename='books')

app_name = 'book'
urlpatterns = [
    path('', include(router.urls)),
]