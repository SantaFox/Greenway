from django.contrib.auth.models import AbstractUser
from django.db import models


class GreenwayUser(AbstractUser):
    ManagingPartner = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    ReferralCode = models.CharField(max_length=50, blank=True)
