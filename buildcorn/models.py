from django.db import models
from django_mysql.models import ListCharField
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
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateField(verbose_name="Start Date", blank=True, null=True)
    end_at = models.DateField(verbose_name="End Date", blank=True, null=True)
    status = models.BooleanField(default=True)
    tenure = models.FloatField(blank=True, null=True, default=0)
    
    # designation = models.CharField(max_length=50, null=True, blank=True)
    # device_name = models.ForeignKey(DeviceName, on_delete = models.CASCADE, blank=True, null=True)
    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f"{self.company}"


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
    Quality = 'Quality'
    Safety = 'Safety' 
    TYPES = ((Quality, 'Quality'),(Safety,'Safety'))
    typee = models.CharField(choices=TYPES, max_length=10)
    ADMIN_STATUS = (('Valid','Valid'),('InValid','InValid'))
    question_id =  models.CharField(default=licenseid, max_length=30)
    question = models.TextField()
    admin_status=models.CharField(choices=ADMIN_STATUS, max_length=10, blank=True, null=True)
    # COMPILED = 'Compiled'
    # UNCOMPLETED = 'Not Compiled'
    # STATUS = ((COMPILED,'Compiled'),(UNCOMPLETED, 'Not Compiled'))
    # status = models.CharField(choices=STATUS, max_length=20, blank=True, null=True)
    # reason = models.TextField(blank=True, null=True)
    # pic = models.ImageField(upload_to="images/page/%Y/%m/%d", verbose_name="Inspection pic", null=True, blank=True)
    def __str__(self):
        return f"{self.typee}=>{self.question}"

class SafetyCheckList(models.Model):
    checklist_id = models.CharField(default=licenseid, max_length=30)
    created_at = models.DateField(auto_now_add=True,blank=True, null=True)
    name = models.CharField(max_length=120)
    question = models.ManyToManyField(Question, blank=True)
    def __str__(self):
        return self.name

class QualityCheckList(models.Model):
    checklist_id = models.CharField(default=licenseid, max_length=30)
    created_at = models.DateField(auto_now_add=True,blank=True, null=True)
    name = models.CharField(max_length=120)
    question = models.ManyToManyField(Question, blank=True)
    def __str__(self):
        return self.name

class AnswerChecklist(models.Model):
    COMPILED = 'Complied'
    UNCOMPLETED = 'Not Complied'
    STATUS = ((COMPILED,'Complied'),(UNCOMPLETED, 'Not Complied'))
    status = models.CharField(choices=STATUS, max_length=20, blank=True, null=True)

    project = models.ForeignKey("Project", on_delete = models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quality_checklist = models.ForeignKey(QualityCheckList, on_delete=models.CASCADE, blank=True, null=True)
    safety_checklist = models.ForeignKey(SafetyCheckList, on_delete=models.CASCADE, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    pic = models.ImageField(upload_to="images/answer/%Y/%m/%d", verbose_name="Inspection pic", null=True, blank=True)
    class Meta:
        ordering = ('-id',)
        unique_together = ["question","quality_checklist","safety_checklist"]
    def __str__(self):
        return f"{self.quality_checklist}=>{self.question.question} "
# Answer.Meta

class Vendor(models.Model):
    ven_id = models.CharField(default=licenseid,max_length=30,blank=True, null=True)
    company = models.ForeignKey(Company, on_delete = models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=15)
    email = models.EmailField(max_length=20)
    contact = PhoneNumberField(unique=True)
    address = models.TextField()
    supervisor_name = models.CharField(max_length=15)
    supervisor_contact = PhoneNumberField(unique=True)
    class Meta:
        ordering = ('-id',)
    def __str__(self):
        return f"{self.name} supervisor is  {self.supervisor_name}"

class Material(models.Model):
    mid =  models.CharField(default=licenseid,max_length=30,blank=True, null=True)
    company = models.ForeignKey(Company, on_delete = models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    maker = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    boq_ref = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    b_uom = models.CharField(max_length=10, blank=True, null=True)
    b_qty = models.PositiveIntegerField(default=0,blank=True, null=True)
    total_uom = models.CharField(max_length=10)
    total_qty = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        ordering = ('-id',)
    def __str__(self):
        return f"{self.name} "



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
    quality_checklist = models.ManyToManyField(QualityCheckList, blank=True, related_name='quality_checklists')
    safety_checklist = models.ManyToManyField(SafetyCheckList, blank=True, related_name='safety_checklists')
    material = models.ManyToManyField(Material, blank=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    class Meta:
        ordering = ("-id",)
        
    def __str__(self):
        return self.name



class Banner(models.Model):
    buildcron_user = models.ForeignKey(User, related_name="banner_buildcron_user", on_delete = models.CASCADE, blank=True, null=True)
    tenent_user = models.ForeignKey(User, related_name="banner_tenent_user", on_delete = models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=30)
    multi_images = models.TextField(blank=True, null=True)
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


class Report(models.Model):
    company = models.ForeignKey(Company, on_delete = models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete =models.CASCADE, blank=True, null=True)
    DONE = 'Done'
    PENDING = 'Pending'
    REPORT_STATUS = ((DONE,'Done'),(PENDING,'Pending'))
    name = models.CharField(max_length=50)
    rid =  models.CharField(default=licenseid,max_length=30,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    typee = models.CharField(max_length=10)
    # project = models.CharField(max_length=50)
    submitted_by = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=REPORT_STATUS, default= PENDING)
    download = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-id",)
    def __str__(self):
        return self.name

# For Mobile purpose
class SiteObservation(models.Model):
    user  = models.ForeignKey(Employee, on_delete=models.CASCADE)
    COMPLIED = 'Complied'
    NOT_COMPLIED = 'Not Complied'
    SITE_OBSERVATION_STATUS = ((COMPLIED,'Complied'),(NOT_COMPLIED,'Not Complied'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    area = models.TextField()
    category = models.CharField(max_length=20,)
    severity = models.CharField(max_length=20,)
    statement = models.TextField()
    status = models.CharField(max_length=15, choices=SITE_OBSERVATION_STATUS, blank=True, null=True)
    is_cleared = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ("-id",)
    # def __str__(self):
    #     return f"{self.user} from {self.user.company}"

