from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from dashboard.models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import status
User = get_user_model()

"""Web level dashboard"""
class ProjectAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id","name","quality_checklist","safety_checklist"]
    def to_representation(self, instance):
        try:
            # context = super(ProjectAnalyticSerializer, self).to_representation(instance)
            return {
                "project_id":instance.id,
                "project_name":instance.name,
            }
        except Exception as e:
            raise serializers.ValidationError({'error':e})

class ProjectAnalyticDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id","name","quality_checklist","safety_checklist"]
    def to_representation(self, instance):
        try:
            context = super(ProjectAnalyticDetailSerializer, self).to_representation(instance)
            total_qulaity_inspections = Report.objects.filter(project=instance,typee=Question.Quality).count()
            total_safety_inspections = Report.objects.filter(project=instance,typee=Question.Safety).count()
            quality_success_count = Report.objects.filter(project=instance,typee=Question.Quality, status=Report.DONE).count()
            safety_success_count = Report.objects.filter(project=instance,typee=Question.Safety, status=Report.DONE).count()
            quality_success_percent = quality_success_count/total_qulaity_inspections*100  if quality_success_count !=0 else 0
            safety_success_percent = safety_success_count/total_safety_inspections*100  if safety_success_count !=0 else 0
            
            site_observation = SiteObservation.objects.filter(project=instance,)
            ncr = NCR.objects.filter(project=instance)
            return {
                "project_id":instance.id,
                "project_name":instance.name,
                "quality":{
                    "total_inspections":total_qulaity_inspections,
                    "success_percent":quality_success_percent,
                    "site_observation": site_observation.filter(category=Question.Quality).count(),
                    "ncr":ncr.filter(category=Question.Quality).count(),
                    # "checklists_by_quality":instance.quality_checklist.values("name"),
                },
                "safety":{
                    "total_inspections":total_safety_inspections,
                    "success_percent":safety_success_percent,
                    "site_observation": site_observation.filter(category=Question.Safety).count(),
                    "ncr":ncr.filter(category=Question.Safety).count(),
                    # "checklists_by_safety":instance.safety_checklist.values("name"),
                }
            }
        except Exception as e:
            raise serializers.ValidationError({'error':e})
# class ChecklistsAnalyticsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ["id","name","quality_checklist","safety_checklist"]
    # def to_representation(self, instance):
    #     try:
    #         context = super(ChecklistsAnalyticsSerializer, self).to_representation(instance)
    #         all_checklist = list(instance.quality_checklist.values("name")) + list(instance.safety_checklist.values("name")) 
    #         result = {}
    #         for i in all_checklist:
    #             if i["name"] not in result:
    #                 result[i.get("name")] =0
    #             result[i["name"]] +=1
    #         print(result)

    #         return {
    #             "checklist_by_quality": all_checklist
    #         }
    #         # return context
    #     except Exception as e:
    #         raise serializers.ValidationError({'error':e})


class ProjectChecklistsUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id","name",]
class ChecklistsUsageSerializer(serializers.ModelSerializer):
    project = ProjectChecklistsUsageSerializer()
    class Meta:
        model = ChecklistsUsage
        fields = ["id","name","count","project","typee"]