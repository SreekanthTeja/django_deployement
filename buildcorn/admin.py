from django.contrib import admin
from .models import *
# Register your models here.

class CheckListAdmin(admin.ModelAdmin):
    list_display=['id','name','typee']


class ProjectAdmin(admin.ModelAdmin):
    list_display=['id','name',]
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(Question)
admin.site.register(Project, ProjectAdmin)
admin.site.register(License)
admin.site.register(Employee)
