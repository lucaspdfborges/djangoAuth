from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    CUSTOMER = 1
    STAFF = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (STAFF, 'Staff'),
        (ADMIN, 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()