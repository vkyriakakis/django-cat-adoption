from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from cats.models import Cat 

class AdoptionRequest(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    
    class Status(models.IntegerChoices):
        PENDING = 1, _("Pending")
        APPROVED = 2, _("Approved")
        REJECTED = 3, _("Rejected")

    status = models.IntegerField(default=Status.PENDING, choices=Status.choices)

    # For rejected requests
    reason = models.CharField(max_length=100, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return "{} wants to adopt {}!".format(self.user, self.cat.name)