from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
import uuid
from django.utils import timezone
# from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, pre_save


# User = get_user_model()

# Create your models here.
def uniqueid():
    return uuid.uuid4().node

class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        # print(email, password)
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
        user.user_type=User.SUPER_ADMIN
        user.save(using= self._db)
        return user


class User(AbstractUser):
    SUPER_ADMIN = 'SA'
    TENENT = 'TN'
    NORMAL_USER='NU'
    USER_TYPE_CHOICES= ((SUPER_ADMIN,'SuperAdmin'), (TENENT,'Tenent'),(NORMAL_USER,'NU'),)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default=NORMAL_USER, max_length=5)
    client_id = models.UUIDField(default=uuid.uuid4().node,)
    phone = models.CharField(max_length=15,null=True, blank=True)
    designation = models.CharField(max_length=30, blank=True, null=True)
    
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

def set_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = uuid.uuid4().node
pre_save.connect(set_username, sender=User)

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_user")
    company_id = models.CharField(default=uniqueid, max_length=30)
    published_date = models.DateField( blank=True, null=True)
    end_at = models.DateField(blank=True, null=True)
    gstin = models.CharField(max_length=50)
    name = models.CharField(max_length=15,null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    status = models.BooleanField(default=True)
    contact_person = models.ForeignKey(User, related_name="contact_person", on_delete=models.CASCADE)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    addres = models.TextField()
    pincode = models.PositiveIntegerField()
    
    employees = models.ManyToManyField(User, blank=True, related_name="company_employee",)
    # projects = models.ManyToManyField(Project, blank=True,related_name="company_projects", )
    
    class Meta:
        ordering = ("-id",)
        
    def __str__(self):
        return self.name

# def send_email_to_admin(sender, instance, **kwargs):
#     if not instance.username:
#         instance.username = uuid.uuid4().node
# pre_save.connect(set_username, sender=User)

    