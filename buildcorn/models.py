from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from accounts.models import Company
from phonenumber_field.modelfields import PhoneNumberField


def licenseid():
    return uuid.uuid4().node

User = get_user_model()

class License(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    license_id = models.CharField(default=licenseid, max_length=20)
    created_at = models.DateField(verbose_name="Start Date", blank=True, null=True)
    end_at = models.DateField(verbose_name="End Date", blank=True, null=True)
    status = models.BooleanField(default=True)
    # designation = models.CharField(max_length=50, null=True, blank=True)
    # tenure = models.FloatField(blank=True, null=True, default=0)
    # device_name = models.ForeignKey(DeviceName, on_delete = models.CASCADE, blank=True, null=True)
    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f"{self.user.first_name}"


# def calculate_tenure(sender,instance,**kwargs):
#     # print(instance, kwargs)
#     created_at = instance.created_at
#     end_at = instance.end_at
#     print(f"{created_at}=={end_at}")
#     from datetime import datetime
#     date_format = "%Y-%m-%d"
#     a = datetime.strptime(str(created_at), date_format)
#     b = datetime.strptime(str(end_at), date_format)
#     difference_in_years = relativedelta(b, a).years
#     print(difference_in_years)
#     instance.tenure = difference_in_years
#     return instance

# post_save.connect(calculate_tenure, sender=License)

class Employee(models.Model):
    eid = models.CharField(default=licenseid, max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="employee_user", blank=True, null=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE, verbose_name="employee_company", blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    class Meta:
        ordering = ("-id",)
    def __str__(self):
        return self.user.email

class Question(models.Model):
    COMPILED = 'Compiled'
    UNCOMPLETED = 'Not Compiled'
    STATUS = ((COMPILED,'Compiled'),(UNCOMPLETED, 'Not Compiled'))
    ADMIN_STATUS = (('Valid','Valid'),('InValid','InValid'))
    question_id =  models.CharField(default=licenseid, max_length=30)
    question = models.TextField()
    admin_status=models.CharField(choices=ADMIN_STATUS, max_length=10, blank=True, null=True)
    status = models.CharField(choices=STATUS, max_length=20, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.question

class CheckList(models.Model):
    Quality = 'Quality'
    Safety = 'Safety' 
    TYPES = ((Quality, 'Quality'),(Safety,'Safety'))
    checklist_id = models.CharField(default=licenseid, max_length=30)
    created_at = models.DateField(auto_now_add=True,blank=True, null=True)
    name = models.CharField(max_length=120)
    typee = models.CharField(choices=TYPES, max_length=10)
    question = models.ManyToManyField(Question, blank=True)
    def __str__(self):
        return self.name

class Project(models.Model):
    company= models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company", blank=True, null=True)
    INSPECTION_DONE='D'
    INSPECTION_PENDING='P'
    INSPECTION_TYPES = ((INSPECTION_DONE,'Done'),(INSPECTION_PENDING,'Pending'))
    name = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)
    approver = models.ForeignKey(Employee, related_name="project_approver", on_delete=models.CASCADE)
    location = models.TextField()
    employee = models.ManyToManyField(Employee, related_name="project_employees", blank=True)
    inspection = models.CharField(choices=INSPECTION_TYPES, max_length=1, blank=True, null=True, default=INSPECTION_PENDING)
    checklists = models.ManyToManyField(CheckList, blank=True, related_name='project_checklists')
    class Meta:
        ordering = ("-id",)
        
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