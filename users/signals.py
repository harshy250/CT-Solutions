from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Profile
from django.contrib.auth.models import User

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user 
        user.delete()
    except User.DoesNotExist:
        print('User deletion is called from CASCADE')

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile) #Whenever profile is updated, trigger this signal
post_delete.connect(deleteUser, sender=Profile)

