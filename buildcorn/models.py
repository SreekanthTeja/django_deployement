from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta


# Create your models here.
def licenseid():
    return uuid.uuid4().node

User = get_user_model()

class DeviceName(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class License(models.Model):
    user_info = models.ForeignKey(User, on_delete = models.CASCADE)
    designation = models.CharField(max_length=50, null=True, blank=True)
    license_id = models.CharField(default=licenseid, max_length=20)
    created_at = models.DateField(verbose_name="Start Date", blank=True, null=True)
    end_at = models.DateField(verbose_name="End Date", blank=True, null=True)
    tenure = models.FloatField(blank=True, null=True, default=0)
    status = models.BooleanField(default=False)
    device_name = models.ForeignKey(DeviceName, on_delete = models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.designation}"


def calculate_tenure(sender,instance,**kwargs):
    # print(instance, kwargs)
    created_at = instance.created_at
    end_at = instance.end_at
    print(f"{created_at}=={end_at}")
    from datetime import datetime
    date_format = "%Y-%m-%d"
    a = datetime.strptime(str(created_at), date_format)
    b = datetime.strptime(str(end_at), date_format)
    difference_in_years = relativedelta(b, a).years
    print(difference_in_years)
    instance.tenure = difference_in_years
    return instance

post_save.connect(calculate_tenure, sender=License)

class CheckList(models.Model):
    checklist_id =  models.CharField(default=licenseid, max_length=30)
    text = models.TextField(default="its a verified list")
    name = models.CharField(max_length=120)
    status = models.BooleanField(default=False, blank=True, null=True)
    def __str__(self):
        return self.name
class QualityLibrary(models.Model):
    TYPE = (('quality','Quality'),('safety','Safety'))
    quality_id = models.CharField(default=licenseid, max_length=30)
    date = models.DateField(auto_now_add=True,blank=True, null=True)
    status = models.BooleanField(default= True)
    name = models.CharField(max_length=120)
    quality_type = models.CharField(choices=TYPE, max_length=10)
    check_list  = models.ManyToManyField(CheckList, blank=True)
    def __str__(self):
        return self.name

class SafetyLibrary(models.Model):
    TYPE = (('quality','Quality'),('safety','Safety'))
    safety_id = models.CharField(default=licenseid, max_length=30)
    date = models.DateField(auto_now_add=True,blank=True, null=True)
    status = models.BooleanField(default= True)
    name = models.CharField(max_length=120)
    quality_type = models.CharField(choices=TYPE, max_length=10)
    check_list  = models.ManyToManyField(CheckList,  blank=True)
    def __str__(self):
        return self.name

class Banner(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    class Meta:
        ordering = ("id",)
    def __str__(self):
        return self.name
    

class FAQ(models.Model):
    faq_id = models.CharField(max_length=50,default=licenseid)
    question = models.CharField(max_length=300)
    answer = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    class Meta:
        ordering = ("id",)
    def __str__(self):
        return self.question