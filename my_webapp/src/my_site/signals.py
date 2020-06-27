## This signal used to add default pic to new registered user
##                       this will be activate when after an object is saved
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import MySiteProfile

## Create profile
@receiver(post_save, sender=User)
def mysite_createProfile(sender, instance, created, **kwargs):
    if created:
        MySiteProfile.objects.create(user=instance)

## Save profile
@receiver(post_save, sender=User)
def mysite_saveProfile(sender, instance, **kwargs):
    instance.mysiteprofile.save()