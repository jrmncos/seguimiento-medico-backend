from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import(
    post_save,
)

from .models import User, Paciente

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    #update user profile
    if created:
        instance.groups.add(Group.objects.get(pk=1))
        Paciente.objects.create(
            user=instance
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.paciente_profile.save()
