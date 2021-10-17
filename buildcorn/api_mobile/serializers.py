from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import status
from .utils import *
# from accounts.api.serializers import UserSerializer
import uuid
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",'first_name','email',"phone_number")
class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model= Employee
        fields = ("id","user")

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
    # approver = EmployeeSerializer()
    # employee = EmployeeSerializer(many=True)
    # safety_checklist = SafetyCheckListSerailizer(many=True)
    # quality_checklist = QualityCheckListSerailizer(many=True)
    # material = MaterialSerializer(many=True)
    class Meta:
        model = Project
        fields = ["id","name",]
    # def to_representation(self, instance):
    #     context = super(ProjectListSerializer, self).to_representation(instance)
    #     """Logic to get queryset"""
    #     checklist_ids = [checklist['id'] for checklist in context['quality_checklist']]
    #     question_ids = [question['id'] for checklists in context['quality_checklist'] for question in checklists["question"]]
    #     answer_obj = AnswerChecklist.objects.filter(project__id=context["id"],quality_checklist__in=checklist_ids,question__in=question_ids,).values()
    #     # print(answer_obj)

    #     status, reason = None,None
    #     """Logic for formating with answers for quality"""
    #     for checklist in context['quality_checklist']:
    #         for que in checklist["question"]:
    #             que["status"] = status
    #             que["reason"] = reason 
    #             try:
    #                 for ans in answer_obj:
    #                     if checklist["id"] == ans["quality_checklist_id"] and ans["question_id"] == que["id"]:
                            
    #                         print(f'{que["id"] }==>{ans["question_id"]}')
    #                         que["status"] = ans["status"]
    #                         que["reason"] = ans["reason"]
    #             except Exception as e:
    #                 raise serializers.ValidationError({'error',e})
                
    #     """Logic for formating with answers for safety"""
    #     s_checklist_ids = [checklist['id'] for checklist in context['safety_checklist']]
    #     s_question_ids = [question['id'] for checklists in context['safety_checklist'] for question in checklists["question"]]
    #     s_answer_obj = AnswerChecklist.objects.filter(project__id=context["id"],safety_checklist__in=s_checklist_ids,question__in=s_question_ids,).values()
    #     # print(s_answer_obj)
    #     for checklist in context['safety_checklist']:
    #         for que in checklist["question"]:
    #             que["status"] = status
    #             que["reason"] = reason
    #             try:
    #                 for ans in s_answer_obj:
    #                     if checklist["id"] == ans["safety_checklist_id"] and ans["question_id"] == que["id"]:
                            
    #                         print(f'{que["id"] }==>{ans["question_id"]}')
    #                         que["status"] = ans["status"]
    #                         que["reason"] = ans["reason"]
    #             except Exception as e:
    #                 raise serializers.ValidationError({'error',e})
    #     return context
class ProjectReadSerializer(serializers.ModelSerializer):
    approver = EmployeeSerializer()
    employee = EmployeeSerializer(many=True)
    safety_checklist = SafetyCheckListSerailizer(many=True)
    quality_checklist = QualityCheckListSerailizer(many=True)
    material = MaterialSerializer(many=True)
    class Meta:
        model = Project
        fields = ["id","name","location","approver","employee","quality_checklist","safety_checklist","material",]
    def to_representation(self, instance):
        context = super(ProjectReadSerializer, self).to_representation(instance)
        """Logic to get queryset"""
        checklist_ids = [checklist['id'] for checklist in context['quality_checklist']]
        question_ids = [question['id'] for checklists in context['quality_checklist'] for question in checklists["question"]]
        answer_obj = AnswerChecklist.objects.filter(project__id=context["id"],quality_checklist__in=checklist_ids,question__in=question_ids,).values()
        

        status, reason = None,None
        """Logic for formating with answers for quality"""
        for checklist in context['quality_checklist']:
             
            for que in checklist["question"]:
                que["status"] = status
                que["reason"] = reason
                try:
                    for ans in answer_obj:
                        if checklist["id"] == ans["quality_checklist_id"] and ans["question_id"] == que["id"]:
                            
                            print(f'{que["id"] }==>{ans["question_id"]}')
                            que["status"] = ans["status"]
                            que["reason"] = ans["reason"]
                            # checklist["area"] = ans["area"]
                except Exception as e:
                    raise serializers.ValidationError({'error',e})
               
        """Logic for formating with answers for safety"""
        s_checklist_ids = [checklist['id'] for checklist in context['safety_checklist']]
        s_question_ids = [question['id'] for checklists in context['safety_checklist'] for question in checklists["question"]]
        s_answer_obj = AnswerChecklist.objects.filter(project__id=context["id"],safety_checklist__in=s_checklist_ids,question__in=s_question_ids,).values()
        # print(s_answer_obj.values("area"))
        for checklist in context['safety_checklist']:
            for que in checklist["question"]:
                que["status"] = status
                que["reason"] = reason
                try:
                    for ans in s_answer_obj:
                        if checklist["id"] == ans["safety_checklist_id"] and ans["question_id"] == que["id"]:
                            
                            # print(f'{que["id"] }==>{ans["question_id"]}')
                            que["status"] = ans["status"]
                            que["reason"] = ans["reason"]
                            # checklist["area"] = ans["area"]
                except Exception as e:
                    raise serializers.ValidationError({'error',e})
        return context



"""Site observation"""

class ProjectForSiteObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields = ['id','name',]
        read_only_fields = ['name']
class VendorForSiteObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields = ['id','name',]
        read_only_fields = ['name']
class SiteObservationSerailizer(WritableNestedModelSerializer):
    project = ProjectForSiteObservationSerializer()
    contractor = VendorForSiteObservationSerializer()
    shedule_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model=SiteObservation
        fields = ("id",'area','project', 'contractor',"status","category","severity","statement", "report","shedule_date")
        read_only_fields = ("id",'project',)
class SiteObservationUpdateSerailizer(WritableNestedModelSerializer):
    project = ProjectForSiteObservationSerializer(required=False)
    contractor = VendorForSiteObservationSerializer(required=False)
    shedule_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model=SiteObservation
        fields = ("id",'area','project', 'contractor',"status","category","severity","statement", "report","shedule_date")
        read_only_fields = ("id",'project',)

"""NCR observation"""
class NCRSerailizer(WritableNestedModelSerializer):
    project = ProjectForSiteObservationSerializer()
    contractor = VendorForSiteObservationSerializer()
    class Meta:
        model=NCR
        fields = ("id",'area','project', 'contractor',"status","reason_to_uncomplied","category","severity","root_cause_number","root_cause", "report",)
        read_only_fields = ("id",'project',)

class NCRUpdateSerailizer(WritableNestedModelSerializer):
    project = ProjectForSiteObservationSerializer(required=False)
    contractor = VendorForSiteObservationSerializer(required=False)
    class Meta:
        model=NCR
        fields = ("id",'area','project', 'contractor',"status","reason_to_uncomplied","category","severity","root_cause_number","root_cause", "report",)
        read_only_fields = ("id",'project',)
        

class ApproverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approver
        fields = ["id","is_approved","submitted_employee","data",]
        read_only_fields = ["id","submitted_employee","data",]
    def to_representation(self, instance):
        context = super(ApproverSerializer, self).to_representation(instance)
        data = json.loads(instance.data)
        context["data"] = data  
        return context