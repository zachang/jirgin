from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from flight.models import Flight

class Book(models.Model):  
    """Represents Book model class"""

    FLIGHT_CLASS = (('BUSINESS', 'B'), ('ECONOMY', 'E'), ('FIRST', 'F'))

    flight_class = models.CharField(max_length=8, choices=FLIGHT_CLASS, default='ECONOMY')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='book')

    class Meta:
        unique_together = (('user', 'flight'),)

    def __str__(self):  
        return "{} class".format(self.flight_class,)
