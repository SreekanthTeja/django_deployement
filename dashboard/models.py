from django.db import models
from accounts.models import Company
from buildcorn.models import Project
# Create your models here.

class ChecklistsUsage(models.Model):
    Quality = 'Quality'
    Safety = 'Safety'
    TYPES = ((Quality, 'Quality'),(Safety,'Safety'))
    typee = models.CharField(choices=TYPES, max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
    class Meta:
        ordering = ("-id",)
    def __str__(self):
        return self.name
