import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Bank

@receiver(post_delete, sender=Bank)
def delete_logo_on_delete(sender, instance, **kwargs):
    if instance.logo and os.path.isfile(instance.logo.path):
        os.remove(instance.logo.path)

@receiver(pre_save, sender=Bank)
def delete_logo_on_change(sender, instance, **kwargs):
    if instance.pk:
        old_logo = Bank.objects.get(pk=instance.pk).logo
        if old_logo and old_logo != instance.logo and os.path.isfile(old_logo.path):
            os.remove(old_logo.path)
