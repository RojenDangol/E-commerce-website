from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver


# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    # print('profile triggered')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            firstname=user.first_name,
            lastname=user.last_name,
        )


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except ObjectDoesNotExist:
        print('User Does not exist.')

    # print('Deleting user...')


post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)
