from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from rest_framework.response import Response
from drf_writable_nested.serializers import WritableNestedModelSerializer
import uuid
User = get_user_model()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class QueSafetyQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id","typee","question"]
""" Safety"""
class SafetySerializer(serializers.ModelSerializer):
    question = QueSafetyQualitySerializer(many=True, required=False)
    class Meta:
        model = SafetyCheckList
        fields = "__all__"
""" Safety ends """
class QualitySerializer(serializers.ModelSerializer):
    question = QueSafetyQualitySerializer(many=True, required=False)
    class Meta:
        model = QualityCheckList
        fields = "__all__"



