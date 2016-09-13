from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gcm_id = models.CharField(max_length=100, blank=True)    
    referral = models.BooleanField(default=False)
    
class Master_Profile(models.Model):
    gcm_id = models.CharField(max_length=100, blank=True)
    
class MenuItem(models.Model):
    item_name = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(default=0)
    image_url = models.CharField(max_length=100, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()
    
