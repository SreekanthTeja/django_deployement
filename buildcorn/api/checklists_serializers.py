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
        # fields = "__all__"
        exclude = ["pic",'admin_status','reason','status']
    def create(self, validated_data):
        data = self.initial_data
        print(data)
        if not data.get('type_id') and data.get('typee'):
            raise serializers.ValidationError({'error':'Type id or Type is missing'})
        type_id, typee = data.pop('type_id'), data.pop('typee')
        try:
            if typee == Question.Quality:
                quality_checklist = QualityCheckList.objects.get(id=type_id,)
                question = Question.objects.create(**data)
                question.save()
                quality_checklist.question.add(question)
                quality_checklist.save()
                return question
            else:
                safety_checklist = SafetyCheckList.objects.get(id=type_id,)
                question = Question.objects.create(**data)
                question.save()
                safety_checklist.question.add(question)
                safety_checklist.save()
                return question
        except Exception as e:
            raise serializers.ValidationError({'status':e})

        # try:
        #     checklist = CheckList.objects.get(id=type_id, typee=typee)
        #     print(checklist)
        #     question = Question.objects.create(**data)
        #     # if created:
        #     question.save()
        #     print(question)

        # except Exception as e:
        #     raise serializers.ValidationError({'status':e})
        # checklist.question.add(question)
        # checklist.save()
        # return question


class QueSafetyQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id","typee","question"]
""" Safety"""
class SafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyCheckList
        fields = "__all__"
class RDSafetySerializer(serializers.ModelSerializer):
    question = QueSafetyQualitySerializer(many=True, required=False)
    class Meta:
        model = SafetyCheckList
        fields = "__all__"
""" Safety ends """
class QualitySerializer(serializers.ModelSerializer):
    # question = QueSafetyQualitySerializer(many=True, required=False)
    class Meta:
        model = QualityCheckList
        fields = "__all__"

class RDQualitySerializer(serializers.ModelSerializer):
    question = QueSafetyQualitySerializer(many=True, required=False)
    class Meta:
        model = QualityCheckList
        fields = "__all__"


