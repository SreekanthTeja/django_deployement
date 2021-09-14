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
        fields = ("email","first_name", "phone_number","id",)

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

class EmployeeSerializer(WritableNestedModelSerializer):
    user = EmployeeUserSerializer()
    company = EmployeeCompanySerializer()
    class Meta:
        model = Employee
        fields = ["id","user","company","designation",]
        read_only_fields = ["id",]




    # def create(self, validated_data):

"""Employee serializer ends"""

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # fields = "__all__"
        exclude = ("employee",)

class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = "__all__" 
        read_only_fields = ( "id","checklist_id",)

    def create(self, validated_data):
        quality = QualityLibrary.objects.get(id=self.initial_data["quality_id"])
        checklist = CheckList.objects.create(**validated_data)
        checklist.save()
        quality.checklist.add(checklist)
        quality.save()
        return checklist

    # def update(self, instance, validated_data):
    #     print(instance)

class QualitySerializer(serializers.ModelSerializer):
    checklist = CheckListSerializer(many =True)
    class Meta:
        model = QualityLibrary
        fields = "__all__" 
        read_only_fields = ('quality_id',"id",)


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



 


