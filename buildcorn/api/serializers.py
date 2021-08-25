from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from rest_framework.response import Response
User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","email","phone","device_name",  "name","address", "city",
                  "state", "gstin", "pincode", "status", "no_licenses")



class LicenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ("user_info", "designation", "license_id","status","created_at","end_at","tenure",)
        read_only_fields = ('license_id',"tenure",)

class LicenseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ("user_info", "designation", "license_id","status","tenure","end_at",)
        read_only_fields = ('license_id', "tenure",)



class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceName
        fields = ("name", "id",)
class LicenseUserSerializer(serializers.ModelSerializer):
    device_name = DeviceSerializer()
    class Meta:
        model = User
        fields = ("username","name","email","phone","device_name")


class LicenseSingleInfoSerializer(serializers.ModelSerializer):
    user_info = LicenseUserSerializer()
    class Meta:
        model = License
        fields = ("user_info", "designation", "license_id","status",)
        read_only_fields = ('license_id', )



class QualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityLibrary
        fields = "__all__" 


class SafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyLibrary
        fields = "__all__" 

class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = "__all__" 
        read_only_fields = ('checklist_id', )

