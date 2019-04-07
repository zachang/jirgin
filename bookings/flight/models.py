from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Flight(models.Model):  
    """Represents Flight model class"""

    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    fly_from = models.CharField(max_length=100)
    fly_to = models.CharField(max_length=100)
    capacity = models.IntegerField(default=10)
    number_booked = models.IntegerField(null=True, default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = (('departure', 'fly_from'),)

    def __str__(self):  
        return "The availability of this flight is {}".format(self.is_available)
