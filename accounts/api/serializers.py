from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.response import Response
from accounts.models import *
from django.db.models import Q
User = get_user_model()


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
    class Meta:
        model = Company
        fields = ("id",'user','name','company_id', 'gstin',"status","pincode","state","city", "addres","license_purchased")
        read_only_fields = ("id",'company_id',"status","license_purchased")
    
    

    
    
    
class CompanyUpdateSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("id",'company_id',)

class PlanSerializer(serializers.ModelSerializer):
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
        def validate(self, attrs):
            credentials = {
                'email': '',
                'password': attrs.get("password")
            }
            username = attrs.get("email")
            password = attrs.get("password")
            if username is None:
                raise serializers.ValidationError('Username must required to login')
            if password is None:
                raise serializers.ValidationError('Password must required to login')
            try:
                user = authenticate(username=username, password= password)
                print(user)
                credentials['email'] = user.email
            except User.DoesNotExist:
                raise serializers.ValidationError('In-valid username or password')
            
            finally:
                data = super().validate(credentials)
                try:
                    company_id = Company.objects.get(user__email=user.email)
                    if company_id:
                        data['email'] = user.email
                        data["first_name"] = user.first_name
                        data['role'] = user.user_type
                        data["company_id"] = company_id.id
                        return data
                except Exception as e:
                    pass
                data['email'] = user.email
                data["first_name"] = user.first_name
                data['role'] = user.user_type
                return data
            

    
