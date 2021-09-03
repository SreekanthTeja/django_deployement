from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
import uuid
from django.utils import timezone
# from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password



# User = get_user_model()

# Create your models here.
def uniqueid():
    return uuid.uuid4().node


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        print(email, password)
        if email:
            email = email
        now = timezone.now()
        user = self.model(
        email=email,
        is_active=True,
        last_login=now,
        date_joined=now,
        **extra_fields
        )

        # password = make_password(password)
        # password = self.check_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        print(email, password)
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
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        ordering = ("-id",)
        
    def __str__(self):
        return self.email
User._meta.get_field("email")._unique=True
User._meta.get_field("username").null=True
User._meta.get_field("phone").null=True
User._meta.get_field("password").null=True

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateField( blank=True, null=True)
    end_at = models.DateField(blank=True, null=True)
    no_licenses = models.PositiveSmallIntegerField(default=0)
    gstin = models.CharField(max_length=50)
    name = models.CharField(max_length=15,null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    status = models.BooleanField(default=True)
    contact_person = models.ForeignKey(User, related_name="contact_person", on_delete=models.CASCADE)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    addres = models.TextField()
    pincode = models.PositiveIntegerField()
    
    # employes = models.ManyToManyField(Employee, blank=True, null=True)
    # projects = models.ManyToManyField(Project, blank=True, null=True)
    
    class Meta:
        ordering = ("-id",)
        
    def __str__(self):
        return self.name

    