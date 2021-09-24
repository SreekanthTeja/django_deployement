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
class LicenseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","first_name","email")

class LicenseSerializer(serializers.ModelSerializer):
    user = LicenseUserSerializer()
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

class CheckListAssignSerailizer(serializers.ModelSerializer):
    # created_at = serializers.DateField(format="%d-%m-%Y",)
    class Meta:
        model=CheckList
        fields = ['id','name','typee','checklist_id','created_at']
class ProjectAssignSerializer(serializers.ModelSerializer):
    checklists = CheckListAssignSerailizer(many=True)

    class Meta:
        model = Project
        fields = ['id','name','checklists']
        
"""Project serializer ends"""


class CheckQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields = ["id","question","admin_status","question_id"]
class CheckListSerializer(serializers.ModelSerializer):
    question = CheckQuestionSerializer(many=True,)
    class Meta:
        model = CheckList
        fields = ["id","checklist_id","typee","name","question",] 
        read_only_fields = ( "id","checklist_id",)
class CheckListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = ["id","checklist_id","typee","name","question",] 
        read_only_fields = ( "id","checklist_id",) 

class CheckListUpdateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = CheckList
        fields = ["id","checklist_id","typee","name","question",] 
        read_only_fields = ( "id","checklist_id",)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        data = self.initial_data
        type_id, typee = data.pop('type_id'), data.pop('typee')
        if not type_id and typee:
            raise serializers.ValidationError({'error':'Type id or Type is missing'})

        try:
            checklist = CheckList.objects.get(id=type_id, typee=typee)
            print(checklist)
            question = Question.objects.create(**data)
            # if created:
            question.save()
            print(question)

        except Exception as e:
            raise serializers.ValidationError({'status':e})
        checklist.question.add(question)
        checklist.save()
        return question
        # # print(checklist)
        # question = Question.objects.get_or_create(question=)
        # checklist.question.

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__" 
        
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

# class SafetyListSerializer(serializers.ModelSerializer):
#     # checklist = SafetyCreateCheckListSerializer(many=True)
#     class Meta:
#         model = SafetyLibrary
#         fields = ('safety_id',"id","name","checklist",) 
#         read_only_fields = ('safety_id',"id","checklist")

# class SafetyCreateCheckListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CheckList
#         fields = ["id","checklist_id","question","answer","status"] 
#         read_only_fields = ( "id","checklist_id",)
#     def create(self, validated_data):
#         safety = SafetyLibrary.objects.get(id=self.initial_data["pid"])
#         checklist = CheckList.objects.create(**validated_data)
#         checklist.save()
#         safety.checklist.add(checklist)
#         safety.save()
#         return checklist


# class SafetyCheckListSerializer(serializers.ModelSerializer):
#     checklist = SafetyCreateCheckListSerializer(many=True)
#     class Meta:
#         model = SafetyLibrary
#         fields = ("id","checklist",) 
#         read_only_fields = ("id","checklist")



# class EmployeeUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("email","first_name","phone_number","id","is_active")
#     def create(self, validated_data):
#         user = User.objects.create_user(password=str(uuid.uuid4().node), **validated_data)
#         user.save()
#         return user

# class EmployeeProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ("name","id",)
#         # read_only_fields = ("name",)
      

# class EmployeeCompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = ("name","id",)
#         read_only_fields = ("name",)
#     def create(self, validated_data):
#         company = Company.license_purchased =- 1
#         company.save()
#         return company

# class EmployeeProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ["id","name"]
        
# class EmployeeSerializer(WritableNestedModelSerializer):
#     user = EmployeeUserSerializer()
#     company = EmployeeCompanySerializer()
#     projects = EmployeeProjectSerializer(required=False,many=True)
#     class Meta:
#         model = Employee
#         fields = ["id","eid","user","company","designation","created_at","projects"]
#         depth = 3
#         read_only_fields = ["id","eid","created_at","projects"]
# class EmployeeCreateSerializer(WritableNestedModelSerializer):
#     user = EmployeeUserSerializer()
#     # company = EmployeeCompanySerializer()
#     class Meta:
#         model = Employee
#         fields = ["id","eid","user","company","designation","created_at",]
#         read_only_fields = ["id","eid","created_at","company"]

# class EmployeeRDUserSerializer(serializers.ModelSerializer):
#     user = EmployeeUserSerializer(required=False)
#     projects = EmployeeProjectSerializer( many=True)
#     class Meta:
#         model = Employee
#         fields = ("id","user","projects")
#         read_only_fields = ["id","user"]

# class EmployeeUpdateUserSerializer(serializers.ModelSerializer):
#     # user = EmployeeUserSerializer(required=False)
#     class Meta:
#         model = User
#         fields = ("id","user","projects")
#         read_only_fields = ["id","user"]







 


