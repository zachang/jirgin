from django.contrib import admin
from django.urls import path, include
from authentication.views import home

urlpatterns = [
    path('', home),
    path('auth/api/', include('authentication.urls', namespace='authentication')),
    path('admin/', admin.site.urls),
]
