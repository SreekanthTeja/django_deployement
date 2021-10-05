from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from rest_framework.response import Response
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import status
from .utils import *
# from accounts.api.serializers import UserSerializer
import uuid
User = get_user_model()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields = ["id","question",]

class SafetyCheckListSerailizer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)
    class Meta:
        model=SafetyCheckList
        fields = ['id','name','question']
class QualityCheckListSerailizer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)
    class Meta:
        model=QualityCheckList
        fields = ['id','name','question']
# #================================================

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("name", )

class MaterialSerializer(serializers.ModelSerializer):
    maker = VendorSerializer()
    class Meta:
        model=Material
        fields = ['id','name',"total_qty","total_uom","maker"]

class ProjectListSerializer(serializers.ModelSerializer):
    safety_checklist = SafetyCheckListSerailizer(many=True)
    quality_checklist = QualityCheckListSerailizer(many=True)
    material = MaterialSerializer(many=True) 
    class Meta:
        model = Project
        fields = ["id","name","location","quality_checklist","safety_checklist","material"]
        
"""Project Inspection starts"""



# class InspectionQualitySerailizer(serializers.ModelSerializer):
#     question = QuestionSerializer(many=True)
#     class Meta:
#         model=QualityCheckList
#         fields = ['id','name','question']
#         read_only_fields = ["name"]

class InspectionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields = ["id","question","status","reason","pic"]

   
class InspectionQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model=AnswerChecklist
        fields = ["id","quality_checklist","status","question","reason"]
        read_only_fields = ["id","question"]
    # def update(self, instance, validated_data):
    #     data = self.initial_data
    #     print(data)
    #     return instance


# class InspectionQualitySerializer(serializers.ModelSerializer):
#     question = QuestionSerializer(many=True)
#     class Meta:
#         model=QualityCheckList
#         fields = ["id","name","question"]
#         read_only_fields = ["id","name",]

#     def update(self, instance, validated_data):
#         data = self.initial_data
#         project = data.get('project',None)
#         checklist  = data.get('checklist',None)
#         user = self.context['request'].user.first_name
#         # project_obj = Project.objects.get(name__exact=data.get('project'))
#         filtering_questions = [que['question'] for que in data.get('question')]
#         que_objs = Question.objects.filter(typee=data.get('type'), question__in=filtering_questions)
#         print(que_objs)
#         # l1 = []
#         # for que in data.get('question'):
#         #     obj = que_objs.get(id=que['id'])
#         #     obj.status = que['status']
#         #     obj.reason = que.get('reason',None)
#         #     l1.append(obj)
#         # que_objs.bulk_update(l1,[ 'status', 'reason'])
#         # compiled_questions_count = que_objs.filter(status=Question.COMPILED).count()
        
#         # if len(que_objs) == compiled_questions_count:
#         #     report = generate_report(status='Done',project=project,checklist=checklist, submitted_by=user,)
#         # else:
#         #     report = generate_report(status='Pending',project=project,checklist=checklist, submitted_by=user,)
#         return instance
        
