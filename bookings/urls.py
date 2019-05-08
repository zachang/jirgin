from django.contrib import admin
from django.urls import path, include
from authentication.views import home

urlpatterns = [
    path("", home),
    path("api/v1/", include("authentication.urls", namespace="authentication")),
    path("api/v1/", include("flight.urls", namespace="flight")),
    path("api/v1/", include("book.urls", namespace="book")),
    path("admin/", admin.site.urls),
]
