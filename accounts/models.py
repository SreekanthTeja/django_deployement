from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
def uniqueid():
    return uuid.uuid4().node

class User(AbstractUser):
    user_id = models.CharField(default=uniqueid, max_length=30)
    phone = models.CharField(max_length=15,null=True, blank=True)
    name = models.CharField(max_length=501)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    state = models.CharField(max_length=50,null=True, blank=True)
    gstin = models.CharField(max_length=50)
    pincode = models.PositiveSmallIntegerField(default=000000)
    status = models.BooleanField(default=True)
    published_date = models.DateField( blank=True, null=True)
    end_at = models.DateField(blank=True, null=True)
    no_licenses = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("-id",)
    def __str__(self):
        return self.username