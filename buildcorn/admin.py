from django.contrib import admin
from .models import *
# Register your models here.

class CheckListAdmin(admin.ModelAdmin):
    list_display=['id','name','typee']
admin.site.register(CheckList, CheckListAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display=['id','name',]
admin.site.register(Project, ProjectAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display=['user','company']  
admin.site.register(Employee, EmployeeAdmin)

admin.site.register(Question)
admin.site.register(License)
