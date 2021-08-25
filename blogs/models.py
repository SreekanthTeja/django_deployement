from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()


class Lead(models.Model):
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    address = models.ForeignKey("Addres", on_delete=models.SET_NULL,null=True, blank=True)
    slug = models.SlugField(max_length = 250, null = True, blank = True, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(f"{self.first_name}_{self.last_name}")
        return super().save(*args, **kwargs)

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
class Addres(models.Model):
    house = models.CharField(max_length=150)
    area = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.city