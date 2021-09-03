from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from accounts.models import *
# User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ("id","client_id","username","email","password","phone",)
        read_only_fields = ("client_id","id",)

    
""" Company register Serializer """
class CompanySerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    user = UserSerializer(many = False)
    class Meta:
        model = Company
        fields = ("id",'user','name', 'gstin',"contact_person","status","published_date","pincode","state","city", "addres", 'end_at',)
        read_only_fields = ("id",)
    def validate(self, data):
        print(data)
        if not  data["user"].get("email"):
            raise serializers.ValidationError('provide email and must be unique')
        if not  data["user"].get("username") :
            raise serializers.ValidationError('provide username  and must be unique')
        if not  data["user"].get("phone") :
            raise serializers.ValidationError('provide phone number')
        if not  data["user"].get("password") :
            raise serializers.ValidationError('provide password')
        if not  data.get("name") :
            raise serializers.ValidationError('provide company name')
        elif not  data.get("gstin"):
            raise serializers.ValidationError('Provide gstin number')
        elif not  data.get("state") :
            raise serializers.ValidationError('provide state')
        elif not  data.get("city") :
            raise serializers.ValidationError('provide city')
        elif not  data.get("pincode") :
            raise serializers.ValidationError('provide pincode')
        elif not  data.get("addres") :
            raise serializers.ValidationError('provide more addres info')
        return data

    def create(self, validated_data):
        user = validated_data.pop('user')
        userobj = {
            'username':user.get("username"),
            'phone':user.get("phone"),
            'email':user.get("email"),
            'password':user.get("password"),
        }
        user = User.objects.create_user(**userobj)
        company = Company.objects.create(user=user, **validated_data)
        company.save()
        return company

    
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     return {"company_name":ret['name']}

class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"