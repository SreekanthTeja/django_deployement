from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from django.utils import timezone
# from django.contrib.auth import get_user_model

# User = get_user_model()

# Create your models here.
def uniqueid():
    return uuid.uuid4().node


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email:
            email = email.lower()
        now = timezone.now()
        user = self.model(
        email=email,
        is_active=True,
        last_login=now,
        date_joined=now,
        **extra_fields
    )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        """creates and saves new super user"""
        user = self.create_user(email, password)
        user.is_staff  = True
        user.is_superuser = True
        user.SUPER_ADMIN=User.SUPER_ADMIN
        user.save(using= self._db)
        return user


class User(AbstractUser):
    SUPER_ADMIN = 'SA'
    TENENT = 'TN'
    USER_TYPE_CHOICES= ((SUPER_ADMIN,'SuperAdmin'), (TENENT,'Tenent'))
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default=TENENT, max_length=5)
    client_id = models.UUIDField(default=uuid.uuid4().node,)
    phone = models.CharField(max_length=15,null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    class Meta:
        ordering = ("-id",)
        
    def __str__(self):
        return self.email
User._meta.get_field("email")._unique=True

class Addres(models.Model):
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    other_info = models.TextField()
    pincode = models.PositiveIntegerField()
    class Meta:
        ordering = ("-id",)
    def __str__(self):
        return f"{self.state} ==> {self.city}"


class Company(models.Model):
    #employes = models.ManyToManyField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateField( blank=True, null=True)
    end_at = models.DateField(blank=True, null=True)
    no_licenses = models.PositiveSmallIntegerField(default=0)
    gstin = models.CharField(max_length=50)
    name = models.CharField(max_length=15,null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    addres = models.ForeignKey(Addres, on_delete = models.SET_NULL, null=True)
    status = models.BooleanField(default=True)
    contact_person = models.ForeignKey(User, related_name="contact_person", on_delete=models.CASCADE)
    
    
    class Meta:
        ordering = ("-id",)
        
    def __str__(self):
        return self.name

    