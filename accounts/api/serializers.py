from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from accounts.models import *
User = get_user_model()

""" Users register Serializer """
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ("id","client_id","first_name","email","password","phone",)
        read_only_fields = ("client_id","id",)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


""" Company register Serializer """
class CompanySerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = ("id",'user','name','company_id', 'gstin',"contact_person","status","published_date","pincode","state","city", "addres", 'end_at',"employees")
        read_only_fields = ("id","employees",)
    def validate(self, data):
        if not  data.get("name") :
            raise serializers.ValidationError('provide company name')
        return data

    

class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"



class CompanyEmployeeListSerializer(serializers.ModelSerializer):
    employees = UserSerializer(many=True)
    class Meta:
        model = Company
        fields = ("id","employees",)

    

class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","email",)


    
