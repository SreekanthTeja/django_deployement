from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from rest_framework.response import Response
from drf_writable_nested.serializers import WritableNestedModelSerializer
User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","user_id","username","email","phone", "name","address", "city",
                  "state", "gstin", "pincode", "status", "no_licenses","published_date","end_at", )
        read_only_fields = ("user_id","id",)

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceName
        fields = ("name", "id",)


class LicenseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","user_id","username","name","email","phone",)
        read_only_fields = ("user_id","id",)
        # lookup_field = 'username'
        

class LicenseListSerializer(serializers.ModelSerializer):
    device_name = DeviceSerializer()
    user_info = LicenseUserSerializer()
    class Meta:
        model = License
        fields = ("id","user_info", "designation", "license_id","status","created_at","end_at","tenure","device_name",)
        read_only_fields = ('license_id',"tenure","id",)


class LicenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ("id","user_info", "designation", "license_id","status","created_at","end_at","tenure","device_name",)
        read_only_fields = ('license_id',"tenure","id",)

    def validate(self, data):
        print(data)
        if not data.get("user_info"):
            raise serializers.ValidationError("Select the candidate")
        if not data.get("end_at"):
            raise serializers.ValidationError("Provide end date")
        elif not data.get("created_at"):
            raise serializers.ValidationError("Provide Start date and must be before end date")
        else:
            return data

    


class LicenseUpdateSerializer(serializers.ModelSerializer):
    # user_info = LicenseUserSerializer()
    class Meta:
        model = License
        fields = ("id","user_info", "designation", "license_id","status","tenure","created_at","end_at","device_name")
        read_only_fields = ('license_id', "tenure","id",)
    def validate(self, data):
        print(data)
        if not data.get("designation"):
            raise serializers.ValidationError("Provide designation")
        if not data.get("end_at"):
            raise serializers.ValidationError("Provide end date")
        elif not data.get("created_at"):
            raise serializers.ValidationError("Provide Start date and must be before end date")
        else:
            return data
    def update(self,instance, validated_data):
        print(instance.user_info)
        user_info = validated_data.pop('user_info')

        
        # instance.user_info.username = user_info.get("username")
        # instance.user_info.name = user_info.get("name")
        # instance.user_info.phone = user_info.get("phone")
        # instance.user_info.email = user_info.get("email")
        
        instance.device_name = validated_data.get("device_name")
        instance.designation = validated_data.get("designation")
        instance.status = validated_data.get("status")
        instance.end_at = validated_data.get("end_at")
        instance.user_info.save()
        instance.save()
        return instance
        
    



class LicenseSingleInfoSerializer(serializers.ModelSerializer):
    user_info = LicenseUserSerializer()
    device_name = DeviceSerializer()
    class Meta:
        model = License
        fields = ("id","user_info", "designation", "license_id","status","tenure","created_at","end_at","device_name",)
        read_only_fields = ('license_id', "tenure","id",)



class QualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityLibrary
        fields = "__all__" 
        read_only_fields = ('quality_id',"id",)


class SafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyLibrary
        fields = "__all__" 
        read_only_fields = ('safety_id', "id",)

class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = "__all__" 
        read_only_fields = ('checklist_id', "id",)


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__" 

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__" 
        read_only_fields = ('faq_id', "id",)



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__" 


class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = "__all__" 
