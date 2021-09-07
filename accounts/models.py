from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from django.utils import timezone
# from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, pre_save
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
def uniqueid():
    return uuid.uuid4().node


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is mandatory')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = uuid.uuid4().node
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('user_type', 'SA')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    SUPER_ADMIN = 'SA'
    TENENT = 'TN'
    NORMAL_USER='NU'
    USER_TYPE_CHOICES= ((SUPER_ADMIN,'SuperAdmin'), (TENENT,'Tenent'),(NORMAL_USER,'NU'),)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default=NORMAL_USER, max_length=5)
    email = models.EmailField(verbose_name="Email Address", max_length=255, unique=True)
    client_id = models.CharField(default=uniqueid,max_length=70, null=True, blank=True)
    phone_number = PhoneNumberField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"
"""Here plans is License"""
class Plan(models.Model):

    name = models.CharField(max_length=50, default="Base Plan")
    license_count = models.PositiveIntegerField(default= 10)
    features = models.TextField(blank=True, null=True, verbose_name = "Features")
    amount = models.FloatField()

    class Meta:
        ordering = ("-id",)
        
    def __str__(self):
        return self.name
        
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_user")
    name = models.CharField(max_length=50, unique = True)
    company_id = models.CharField(default=uniqueid, max_length=50)
    gstin = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=False)
    contact_person = models.ForeignKey(User, related_name="contact_person", on_delete=models.CASCADE)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    addres = models.TextField(verbose_name = "Address", blank=True, null=True)
    pincode = models.PositiveIntegerField()
    payment_success = models.BooleanField(default = False, blank=True, null=True)

    class Meta:
        ordering = ("-id",)
        
    def __str__(self):
        return self.name





# def send_email_to_admin(sender, instance, **kwargs):
#     if not instance.username:
#         instance.username = uuid.uuid4().node
# pre_save.connect(set_username, sender=User)