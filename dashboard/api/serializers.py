from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import status
User = get_user_model()

"""Web level dashboard"""
class ProjectAnalyticSerializer(serializers.ModelSerializer):
    # safety_checklist = SafetyCheckListSerailizer(many=True)
    # quality_checklist = QualityCheckListSerailizer(many=True)
    # material = MaterialSerializer(many=True)
    class Meta:
        model = Project
        fields = ["id","name","location","quality_checklist","safety_checklist","material",]
    def to_representation(self, instance):
        try:
            context = super(ProjectAnalyticSerializer, self).to_representation(instance)
            total_qulaity_inspections = Report.objects.filter(project=instance,typee=Question.Quality).count()
            total_safety_inspections = Report.objects.filter(project=instance,typee=Question.Safety).count()
            quality_success_count = Report.objects.filter(project=instance,typee=Question.Quality, status=Report.DONE).count()
            safety_success_count = Report.objects.filter(project=instance,typee=Question.Safety, status=Report.DONE).count()
            quality_success_percent = quality_success_count/total_qulaity_inspections*100  if quality_success_count !=0 else 0
            safety_success_percent = safety_success_count/total_safety_inspections*100  if safety_success_count !=0 else 0
            
            return {
                "project_id":instance.id,
                "project_name":instance.name,
                "quality":{
                    "type":"Quality",
                    "total_inspections":total_qulaity_inspections,
                    "success_percent":f"{quality_success_percent}%",
                },
                "safety":{
                    "type":"Safety",
                    "total_inspections":total_safety_inspections,
                    "success_percent":f"{safety_success_percent}%"
                }
            }
        except Exception as e:
            raise serializers.ValidationError({'error':e})
        