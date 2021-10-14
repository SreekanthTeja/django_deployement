from django.contrib import admin
from .models import *
# Register your models here.

class QualityCheckListAdmin(admin.ModelAdmin):
    list_display=['id','name',]
admin.site.register(QualityCheckList, QualityCheckListAdmin)

class SafetyCheckListAdmin(admin.ModelAdmin):
    list_display=['id','name',]
admin.site.register(SafetyCheckList, SafetyCheckListAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display=['id','name',]
admin.site.register(Project, ProjectAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display=['user','company']  
admin.site.register(Employee, EmployeeAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display=['question','typee']  
admin.site.register(Question, QuestionAdmin)

admin.site.register(AnswerChecklist)
admin.site.register(License)

admin.site.register(Vendor)
admin.site.register(TenentBanner)
admin.site.register(Banner)
admin.site.register(Material)
admin.site.register(Approver)
admin.site.register(Report)

class SiteObservationAdmin(admin.ModelAdmin):
    list_display=['user','project','get_project',]
    @admin.display(description='Company')
    def get_project(self, obj):
        return obj.project.company.name
admin.site.register(SiteObservation, SiteObservationAdmin)

class NCRAdmin(admin.ModelAdmin):
    list_display=['user','project','get_project',]
    @admin.display(description='Company')
    def get_project(self, obj):
        return obj.project.company.name
admin.site.register(NCR, NCRAdmin)