from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers, status
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.response import Response
from rest_framework.parsers import ParseError
from accounts.models import *
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination as PageSize
User = get_user_model()



class CustomPageSize(PageSize):
    page_size_query_param = '10'
""" Users  Serializer """

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ("id","client_id","first_name","email","phone_number",'password')
        read_only_fields = ("client_id","id","password",)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.user_type = User.TENENT
        user.save()
        return user


""" Company register Serializer """
class CompanySerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    user = UserSerializer()
    pagination_class = CustomPageSize
    class Meta:
        model = Company
        fields = ("id",'user','name','company_id', 'gstin',"status","pincode","state","city", "addres","license_purchased")
        read_only_fields = ("id",'company_id',"status",)
    
    
class CompanyUpdateSerializer(WritableNestedModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Company
        fields =("id",'user','name','company_id', 'gstin',"status","pincode","state","city", "addres","license_purchased")
        read_only_fields = ("id",'user','company_id',"status")

class PlanSerializer(serializers.ModelSerializer):
    pagination_class = CustomPageSize
    class Meta:
        model = Plan
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

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    {
        "email":"david@gmail.com",
        "password":"test1234" 
    }
    """
    def validate(self, attrs):
        credentials = {
            'email': '',
            'password': attrs.get("password")
        }
        username = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(username=username, password= password)
        if not user:
            raise ParseError({'error':'In-valid username or password'})
        credentials['email'] = user.email
        data = super().validate(credentials)
        try:
            company_id = Company.objects.get(user__email=user.email)
            if company_id:
                data['email'] = user.email
                data["first_name"] = user.first_name
                data['role'] = user.user_type
                data["company_id"] = company_id.id
                data["company_name"] = company_id.name
                data["license_count"] = company_id.license_purchased
                return data
        except Exception as e:
            data['email'] = user.email
            data["first_name"] = user.first_name
            data['role'] = user.user_type
        return data
            
"""Password reset"""

class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    

class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"







