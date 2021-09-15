from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from rest_framework.response import Response
from drf_writable_nested.serializers import WritableNestedModelSerializer
from accounts.api.serializers import UserSerializer
import uuid
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name","email")

class LicenseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = License
        fields = "__all__"

"""Employee serializer"""

class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email","first_name","id",)

    def create(self, validated_data):
        user = User.objects.create_user(password=str(uuid.uuid4().node), **validated_data)
        user.save()
        return user

class EmployeeCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("name","id",)
        read_only_fields = ("name",)
    def create(self, validated_data):
        company = Company.license_purchased =- 1
        company.save()
        return company

class EmployeeProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id","name"]
class EmployeeSerializer(WritableNestedModelSerializer):
    user = EmployeeUserSerializer()
    company = EmployeeCompanySerializer()
    projects = EmployeeProjectSerializer(many=True)
    class Meta:
        model = Employee
        fields = ["id","eid","user","company","designation","projects","created_at","projects"]
        read_only_fields = ["id","eid","created_at","projects"]
class EmployeeCreateSerializer(WritableNestedModelSerializer):
    user = EmployeeUserSerializer()
    company = EmployeeCompanySerializer()
    class Meta:
        model = Employee
        fields = ["id","eid","user","company","designation","projects","created_at",]
        read_only_fields = ["id","eid","created_at"]

class EmployeeUpdateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Employee
        # fields = ["id","eid","user","company","designation","projects","created_at"]
        # read_only_fields = ["id","eid","created_at"]
        exclude = ["user"]

    # def create(self, validated_data):

"""Employee serializer ends"""

"""Project serializer starts"""
class ApproverSerializer(serializers.ModelSerializer):
    user = EmployeeUserSerializer()
    class Meta:
        model=Employee
        fields = ("id","user",)
class ProjectListSerializer(serializers.ModelSerializer):
    approver = ApproverSerializer()
    employee = ApproverSerializer(many=True)
    class Meta:
        model = Project
        fields = "__all__"
class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
"""Project serializer ends"""

class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = ["id","checklist_id","question","answer","status"] 
        read_only_fields = ( "id","checklist_id",)

    def create(self, validated_data):
        quality = QualityLibrary.objects.get(id=self.initial_data["qid"])
        checklist = CheckList.objects.create(**validated_data)
        checklist.save()
        quality.checklist.add(checklist)
        quality.save()
        return checklist

    # def update(self, instance, validated_data):
    #     print(instance)


"""Quality starts"""
class QualityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityLibrary
        fields = "__all__" 
        read_only_fields = ('quality_id',"id",)
class QualityListSerializer(serializers.ModelSerializer):
    checklist = CheckListSerializer(many=True)
    class Meta:
        model = QualityLibrary
        fields = ('quality_id',"id","name","checklist",) 
        read_only_fields = ('quality_id',"id","checklist")

class RUDQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityLibrary
        fields = ("id","name")
        read_only_fields = ("id",)

class QualityCheckListSerializer(serializers.ModelSerializer):
    checklist = CheckListSerializer(many=True)
    class Meta:
        model = QualityLibrary
        fields = ("id","checklist",) 
        read_only_fields = ("id","checklist")
"""Quality ends"""

class SafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyLibrary
        fields = "__all__" 
        read_only_fields = ('safety_id', "id",)




class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__" 

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__" 
        read_only_fields = ('faq_id', "id",)



 


