from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# when a user is saved, send this signal, the reciever is the function below
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Everytime a user is created, created the associated profile"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Everytime a user is created, created the associated profile"""
    instance.profile.save()