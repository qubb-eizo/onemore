from account.models import User

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    # instance.profile.save()
    if created:
        User.objects.create(user=instance)
    else:
        instance.profile.save()
