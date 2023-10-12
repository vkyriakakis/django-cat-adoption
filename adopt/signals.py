from django.db import models
from django.contrib.auth.models import Group, User
from django.dispatch import receiver

from adopt.models import AdoptionRequest

@receiver(models.signals.post_save, sender=AdoptionRequest)
def mark_other_adoptions_as_rejected(sender, instance, created, **kwargs):
    # If an adoption request for a cat is approved,
    # all other adoption requests for that cat should
    # be marked as REJECTED
    if instance.status == AdoptionRequest.Status.APPROVED:
        AdoptionRequest.objects.filter(cat=instance.cat) \
                               .exclude(id=instance.id) \
                               .update(status=AdoptionRequest.Status.REJECTED)