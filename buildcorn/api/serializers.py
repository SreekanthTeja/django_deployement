from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from rest_framework.response import Response
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from accounts.api.serializers import UserSerializer
import uuid
User = get_user_model()

"""License """
class LicenseCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("name","gstin","license_purchased")
    def to_representation(self, instance):
        print(instance)
        context = super(LicenseCompanySerializer, self).to_representation(instance)
        license_used_count = Employee.objects.filter(company=instance).values('user').count()
        # if context['license_purchased'] == license_used_count:
        #     raise serializers.ValidationError({'status':'Your quota is completed'})
        return {
            'name':context["name"],
            'gstin':context['gstin'],
            'total_licenses':context['license_purchased'],
            'license_used_count':license_used_count
        }

class LicenseSerializer(serializers.ModelSerializer):
    company = LicenseCompanySerializer()
    class Meta:
        model = License
        fields = "__all__"
"""License ends """

"""Normal user"""

class EmployeeUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ("id","first_name","email", "phone_number","is_active",)
        read_only_fields = ("id",)
    def create(self, validated_data):
        user = User.objects.create_user(password=str(uuid.uuid4().node), **validated_data)
        # user = User.objects.create_user(**validated_data)
        user.save()
        return user
class EmployeeSerializer(WritableNestedModelSerializer):
    user = EmployeeUserSerializer()
    class Meta:
        model = Employee
        fields = ("id","user",'eid', "company","created_at")
        read_only_fields = ("id",'eid',"created_at")
"""Normal user ends"""


"""Project serializer starts"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",'first_name','email',)
class ApproverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model= Employee
        fields = ("id","user")


class ProjectListSerializer(serializers.ModelSerializer):
    approver = ApproverSerializer()
    employee = ApproverSerializer(many=True)
    class Meta:
        model = Project
        fields = "__all__"
class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
"""Project serializer ends"""

"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
class QuestionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields = ['id',"question"]

class QualityDataSerializer(serializers.ModelSerializer):
    question = QuestionDataSerializer(many=True)
    class Meta:
        model=QualityCheckList
        fields = ['id','name',"question"]

class SafetyDataSerializer(serializers.ModelSerializer):
    question = QuestionDataSerializer(many=True)
    class Meta:
        model=SafetyCheckList
        fields = ['id','name',"question"]
class ShowQualityProjectSerializer(serializers.ModelSerializer):
    quality_checklist = SafetyDataSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id','name','quality_checklist']
        
class ShowSafetyProjectSerializer(serializers.ModelSerializer):
    safety_checklist = QualityDataSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id','name','safety_checklist']
"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"



class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'



class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("id","name", )
        read_only_fields=("name",)

class MaterialCreateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"

class MaterialRUDSerializer(WritableNestedModelSerializer):
    maker = VendorSerializer(required=False,)
    class Meta:
        model = Material
        fields = "__all__"


    # def update(self, instance, validated_data):
    #     print(validated_data)
        
        # exclude = ['maker']
# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = '__all__'

#     def create(self, validated_data):
#         data = self.initial_data
#         type_id, typee = data.pop('type_id'), data.pop('typee')
#         if not type_id and typee:
#             raise serializers.ValidationError({'error':'Type id or Type is missing'})

#         try:
#             checklist = CheckList.objects.get(id=type_id, typee=typee)
#             print(checklist)
#             question = Question.objects.create(**data)
#             # if created:
#             question.save()
#             print(question)

#         except Exception as e:
#             raise serializers.ValidationError({'status':e})
#         checklist.question.add(question)
#         checklist.save()
#         return question


