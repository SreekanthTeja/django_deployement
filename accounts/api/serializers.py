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
# class AddresSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Addres
#         fields = "__all__"




""" Company register Serializer """
class CompanySerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    user = UserSerializer(many = False)
    class Meta:
        model = Company
        fields = ("id",'user','name', 'gstin',"contact_person","status","published_date","pincode","state","city", "addres", 'end_at',)
        read_only_fields = ("id",)
    # def validate(self, data):
    #     if not  data.get("user") :
    #         raise serializers.ValidationError('User must required ')
    #     elif not  data.get("name"):
    #         raise serializers.ValidationError('Provide company name')
    #     return data

    def create(self, validated_data):
        user = validated_data.pop('user')
        # addres =validated_data.pop('addres')

        userobj = {
            'username':user.get("username"),
            'phone':user.get("phone"),
            'email':user.get("email"),
            'password':user.get("password"),
        }
        # addresobj = {
        #     'state':addres.get("state"),
        #     'city':addres.get("city"),
        #     'other_info':addres.get("other_info"),
        #     'pincode':addres.get("pincode"),
        # }
        user = User.objects.create_user(**userobj)
        # addres = Addres.objects.create(**addresobj)
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