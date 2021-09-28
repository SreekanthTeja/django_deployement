from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from rest_framework.response import Response
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from accounts.api.serializers import UserSerializer
import uuid
User = get_user_model()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields = ["id","question","status","reason","pic"]

class SafetyCheckListSerailizer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)
    class Meta:
        model=SafetyCheckList
        fields = ['id','name','question']
class QualityCheckListSerailizer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)
    class Meta:
        model=QualityCheckList
        fields = ['id','name','question']
# #================================================

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("name", )

class MaterialSerializer(serializers.ModelSerializer):
    maker = VendorSerializer()
    class Meta:
        model=Material
        fields = ['id','name',"total_qty","total_uom","maker"]

class ProjectListSerializer(serializers.ModelSerializer):
    safety_checklist = SafetyCheckListSerailizer(many=True)
    quality_checklist = QualityCheckListSerailizer(many=True)
    material = MaterialSerializer(many=True) 
    class Meta:
        model = Project
        fields = ["id","name","location","quality_checklist","safety_checklist","material"]
        


