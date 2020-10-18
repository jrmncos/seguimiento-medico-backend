from django.dispatch import receiver
from django.db.models.signals import(
    post_save,
)

from .models import User, Paciente

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    #update user profile
    if created:
        Paciente.objects.create(
            user=instance
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.paciente_profile.save()