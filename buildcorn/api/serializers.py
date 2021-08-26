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
        fields = ("user_id","username","email","phone", "name","address", "city",
                  "state", "gstin", "pincode", "status", "no_licenses", )
        read_only_fields = ("user_id",)

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceName
        fields = ("name", "id",)


class LicenseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id","username","name","email","phone",)
        read_only_fields = ("user_id",)

class LicenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ("user_info", "designation", "license_id","status","created_at","end_at","tenure","device_name",)
        read_only_fields = ('license_id',"tenure",)

    def validate(self, data):
        print(data)
        if not data["end_at"]:
            raise serializers.ValidationError("Provide end date")
        elif not data["created_at"]:
            raise serializers.ValidationError("Provide Start date")
        else:
            return data

    


class LicenseUpdateSerializer(serializers.ModelSerializer):
    user_info = LicenseUserSerializer()
    class Meta:
        model = License
        fields = ("user_info", "designation", "license_id","status","tenure","created_at","end_at","device_name")
        read_only_fields = ('license_id', "tenure",)
    
    def update(self,instance, validated_data):
        print(instance)
        user_info = validated_data.pop('user_info')
        instance.user_info.username = user_info.get("username")
        instance.user_info.name = user_info.get("name")
        instance.user_info.phone = user_info.get("phone")
        instance.user_info.email = user_info.get("email")
        
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
        fields = ("user_info", "designation", "license_id","status","tenure","created_at","end_at","device_name",)
        read_only_fields = ('license_id', "tenure",)



class QualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityLibrary
        fields = "__all__" 
        read_only_fields = ('quality_id', )


class SafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyLibrary
        fields = "__all__" 
        read_only_fields = ('safety_id', )

class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = "__all__" 
        read_only_fields = ('checklist_id', )

