from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class DeviceName(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class User(AbstractUser):
    phone = models.CharField(max_length=15,null=True, blank=True)
    name = models.CharField(max_length=501)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    state = models.CharField(max_length=50,null=True, blank=True)
    gstin = models.CharField(max_length=50)
    pincode = models.PositiveSmallIntegerField(default=000000)
    status = models.BooleanField(default=True)
    published_date = models.DateField(auto_now_add=True, blank=True, null=True)
    no_licenses = models.PositiveSmallIntegerField(default=0)
    device_name = models.ForeignKey(DeviceName, on_delete = models.CASCADE, blank=True, null=True)


    class Meta:
        ordering = ("-id",)
    def __str__(self):
        return self.name