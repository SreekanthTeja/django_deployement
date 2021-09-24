from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from rest_framework.response import Response
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from accounts.api.serializers import UserSerializer
import uuid
User = get_user_model()





# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Question
#         fields = ["id","question",]

# class CheckListSerailizer(serializers.ModelSerializer):
#     question = QuestionSerializer(many=True)
#     class Meta:
#         model=CheckList
#         fields = ['id','name','typee','question']
# #================================================

# class ProjectListSerializer(serializers.ModelSerializer):
#     checklists = CheckListSerailizer(many=True)
#     class Meta:
#         model = Project
#         fields = ["id","name","location","checklists"]


