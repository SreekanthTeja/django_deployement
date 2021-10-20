from django.db import models
from django_mysql.models import ListCharField
from django.contrib.auth import get_user_model
import uuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from accounts.models import Company
from phonenumber_field.modelfields import PhoneNumberField
from buildcorn.signals import generate_report


def licenseid():

    return uuid.uuid4().node

User = get_user_model()


class License(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateField(verbose_name="Start Date", blank=True, null=True)
    end_at = models.DateField(verbose_name="End Date", blank=True, null=True)
    status = models.BooleanField(default=True)
    tenure = models.FloatField(blank=True, null=True, default=0)
    emp_license_ids = models.TextField(blank=True, null=True)
    last_license_id = models.IntegerField(blank=True, null=True, default=0)
    
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

def license_assign(sender, instance, **kwargs):
    # id = self.initial_data["lid"]['id']
    # comp = Company.objects.get(user__email=self.context["request"].user)
    # print(validated_data)

    # lic_obj = License.objects.get(company=comp)
    # lic_json_loads = json.loads(lic_obj.emp_license_ids)
    # for i in lic_json_loads:
    #     if i["id"] == id:
    #         i["active"]= False
    # json_dumps = json.dumps(lic_json_loads)
    # lic_obj.emp_license_ids = json_dumps
    # lic_obj.save()
    print("{}/{}/{}".format(kwargs, instance, sender))
class Employee(models.Model):
    lid = models.CharField(blank=True, null=True, verbose_name="Employee license", max_length=50)
    eid = models.CharField(default=licenseid, max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="employee_user", blank=True, null=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE, verbose_name="employee_company", blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    license_approved = models.BooleanField(blank=True, null=True)
    
    class Meta:
        ordering = ("-id",)
    def __str__(self):
        return self.user.email
#     def save(self, *args, **kwargs):
#         print(self)
#         super(Employee, self).save(*args, **kwargs)
# pre_save.connect(license_assign, sender=Employee)



class Question(models.Model):
    Quality = 'Quality'
    Safety = 'Safety'
    TYPES = ((Quality, 'Quality'),(Safety,'Safety'))
    typee = models.CharField(choices=TYPES, max_length=10)
    ADMIN_STATUS = (('Valid','Valid'),('InValid','InValid'))
    question_id =  models.CharField(default=licenseid, max_length=30)
    question = models.TextField()
    admin_status=models.CharField(choices=ADMIN_STATUS, max_length=10, blank=True, null=True)
    def __str__(self):
        return f"{self.typee}=>{self.question}"

class SafetyCheckList(models.Model):
    checklist_id = models.CharField(default=licenseid, max_length=30)
    created_at = models.DateField(auto_now_add=True,blank=True, null=True)
    name = models.CharField(max_length=120)
    # is_approved = models.BooleanField(default=False, blank=True, null=True)
    question = models.ManyToManyField(Question, blank=True)
    def __str__(self):
        return self.name

class QualityCheckList(models.Model):
    checklist_id = models.CharField(default=licenseid, max_length=30)
    created_at = models.DateField(auto_now_add=True,blank=True, null=True)
    name = models.CharField(max_length=120)
    # is_approved = models.BooleanField(default=False, blank=True, null=True)
    question = models.ManyToManyField(Question, blank=True)
    def __str__(self):
        return self.name

# class SiteDetails(models.Model):
#     area = models.TextField(blank=True, null=True)
#     vendor = models.ForeignKey("Vendor", on_delete = models.CASCADE, blank=True, null=True)
#     def __str__(self):
#         return self.area

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
    shedule_date = models.DateTimeField(blank=True, null=True)
    # site_details = models.ForeignKey(SiteDetails, on_delete=models.CASCADE, blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    vendor = models.ForeignKey("Vendor", on_delete = models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        unique_together = ["question","quality_checklist","safety_checklist"]
    def __str__(self):
        return f"{self.project.name}=>{self.question.question} "


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


"""Mobile purpose"""
class Approver(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Approver")
    project = models.ForeignKey(Project, related_name="mobile_approver", on_delete = models.CASCADE)
    submitted_employee = models.ForeignKey(Employee, on_delete = models.CASCADE, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    # created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    # updated_at = models.DateField(auto_now=True)
    class Meta:
        ordering = ('-id',)
    def __str__(self):
        return f"{self.user.first_name}"
post_save.connect(generate_report, sender=Approver)

class TenentBanner(models.Model):
    company = models.ForeignKey(Company, on_delete= models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    tenent_images = models.TextField(blank=True, null=True)
    class Meta:
        ordering = ("id",)
    def __str__(self):
        return self.company.name
class Banner(models.Model):
    buildcron_user = models.ForeignKey(User, related_name="banner_buildcron_user", on_delete = models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=30)
    multi_images = models.TextField(blank=True, null=True)
    class Meta:
        ordering = ("-id",)
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
    status = models.CharField(max_length=15, choices=SITE_OBSERVATION_STATUS, blank=True, null=True)
    reason_to_uncomplied = models.TextField(blank=True, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    area = models.TextField()
    category = models.CharField(max_length=20,)
    severity = models.CharField(max_length=20,)
    statement = models.TextField()
    is_cleared = models.BooleanField(default=False, blank=True, null=True)
    report = models.FileField(upload_to="siteobservation/", blank=True, null=True)
    shedule_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("-id",)
    # def __str__(self):
    #     return f"{self.user.company.name}"
        # return self.project.company.name

class NCR(models.Model):
    COMPLIED = 'Complied'
    NOT_COMPLIED = 'Not Complied'
    NCR_STATUS = ((COMPLIED,'Complied'),(NOT_COMPLIED,'Not Complied'))
    status = models.CharField(max_length=15, choices=NCR_STATUS, blank=True, null=True)
    reason_to_uncomplied = models.TextField(blank=True, null=True,)

    user  = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    area = models.TextField()
    category = models.CharField(max_length=20,)
    severity = models.CharField(max_length=20,)
    root_cause = models.TextField()
    root_cause_number = models.CharField(max_length=50,blank=True, null=True)
    recomended_action = models.TextField()
    is_cleared = models.BooleanField(default=False, blank=True, null=True)

    report = models.FileField(upload_to="NCR/", blank=True, null=True)
    shedule_date = models.DateTimeField(blank=True, null=True)
    satiffaction_status = models.CharField(choices=NCR_STATUS, max_length=15, blank=True, null=True)
    reason_to_satiffaction_status = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.project.company.name


