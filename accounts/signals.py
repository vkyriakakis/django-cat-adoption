from django.db import models
from django.contrib.auth.models import Group, User
from django.dispatch import receiver

@receiver(models.signals.m2m_changed, sender=User.groups.through)
def give_admin_page_access_to_staff(sender, instance, action, **kwargs):
    # If a user is added to the Staff group, give access to the admin page
    if action == "post_add" and Group.objects.filter(user=instance, name="Staff").exists():
        instance.is_staff = True
        instance.save()
    # If they are removed, withdraw the access as well
    elif action == "post_remove" and not Group.objects.filter(user=instance, name="Staff").exists():
        instance.is_staff = False
        instance.save()