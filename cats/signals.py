from django.db import models
from django.contrib.auth.models import Group, User
from django.dispatch import receiver

from adopt.models import AdoptionRequest

@receiver(models.signals.post_save, sender=AdoptionRequest)
def mark_cat_as_adopted(sender, instance, created, **kwargs):
    # If an adoption request for a cat is approved,
    # that cat should be marked as adopted
    if instance.status == AdoptionRequest.Status.APPROVED:
        cat = instance.cat
        cat.is_adopted = True
        cat.save()