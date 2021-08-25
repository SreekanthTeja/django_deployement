from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Create your models here.
def licenseid():
    return uuid.uuid4().node

User = get_user_model()

# class UserRegistration(models.Model):
#     user = models.ForeignKey(User, on_delete = models.CASCADE)
    
#     class Meta:
#         ordering = ("-id",)
#     def __str__(self):
#         return self.name

class License(models.Model):
    user_info = models.ForeignKey(User, on_delete = models.CASCADE)
    designation = models.CharField(max_length=50, null=True, blank=True)
    license_id = models.CharField(default=licenseid, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.designation}"


class CheckList(models.Model):
    checklist_id =  models.CharField(default=licenseid, max_length=30)
    text = models.TextField(default="its a verified list")
    name = models.CharField(max_length=120)
    def __str__(self):
        return self.name
class QualityLibrary(models.Model):
    TYPE = (('bad','Bad'),('good','Good'),('moderate','Moderate'))
    date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default= True)
    name = models.CharField(max_length=120)
    quality_type = models.CharField(choices=TYPE, max_length=10)
    check_list  = models.ManyToManyField(CheckList)
    def __str__(self):
        return self.name