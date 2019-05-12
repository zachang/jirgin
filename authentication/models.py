from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from cloudinary.uploader import destroy


class UserProfile(models.Model):
    """Represents UserProfile model class"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True)

    def __str__(self):
        return "{}'s profile".format(self.user)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
