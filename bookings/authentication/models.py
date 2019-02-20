from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):  
    """Represents UserProfile model class"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):  
          return "{}'s profile".format(self.user,)

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)
