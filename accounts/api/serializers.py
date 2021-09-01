from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from accounts.models import *
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","client_id","username","email","password","phone",)
        read_only_fields = ("client_id","id",)
class AddresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addres
        fields = "__all__"

""" Company register Serializer """
class CompanySerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    addres = AddresSerializer()
    
    class Meta:
        model = Company
        fields = ( 'user', 'name', 'gstin',"contact_person","status","published_date", "addres", 'end_at',)

    def validate(self, data):
        if not  data.get("user") :
            raise serializers.ValidationError('User must required ')
        elif not  data.get("name"):
            raise serializers.ValidationError('Provide company name')
        return data

    
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     return {"company_name":ret['name']}

class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"