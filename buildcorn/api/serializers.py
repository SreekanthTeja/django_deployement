from rest_framework import serializers
from django.contrib.auth import get_user_model
from buildcorn.models import *
from accounts.models import *
from rest_framework.response import Response
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.core.files.storage import FileSystemStorage
import datetime
from django.conf import settings
# from accounts.api.serializers import UserSerializer
import uuid
import os
import json
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



"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
class QuestionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields = ['id',"question"]

class QualityDataSerializer(serializers.ModelSerializer):
    question = QuestionDataSerializer(many=True)
    class Meta:
        model=QualityCheckList
        fields = ['id','name',"question","checklist_id"]

class SafetyDataSerializer(serializers.ModelSerializer):
    question = QuestionDataSerializer(many=True)
    class Meta:
        model=SafetyCheckList
        fields = ['id','name',"checklist_id","question"]
class ShowQualityProjectSerializer(serializers.ModelSerializer):
    quality_checklist = QualityDataSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id','name','quality_checklist']
        
class ShowSafetyProjectSerializer(serializers.ModelSerializer):
    safety_checklist = SafetyDataSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id','name','safety_checklist']
"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"



class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

    def validate(self, data):
        images = self.context['request'].FILES
        # print(len(images.getlist('image')))
        if len(images.getlist('image')) > 2:
            raise serializers.ValidationError({'error':"Select minimum 2 images"})
        return data

    def create(self, validated_data):
        # images = self.context['request'].FILES
        picture = self.context['request'].FILES.getlist('image')
        all_pictures = []
        for pic in picture:
            location = '%s/banner'%(settings.MEDIA_ROOT)
            fs = FileSystemStorage(location=location)
            picname = "IMG_%s.jpg"%(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'))
            f_save = fs.save(picname, pic)
            filepath = "%s/%s"%(location,picname)
            all_pictures.append(filepath)
        all_pictures = json.dumps(all_pictures)
        if self.context['request'].user.user_type == User.SUPER_ADMIN:
            user = User.objects.get(email=self.context['request'].user.email)
            banner = Banner.objects.create(name=validated_data.get('name',None),buildcron_user=user, multi_images=all_pictures)
            return banner
        else:
            user = User.objects.get(email=self.context['request'].user.email)
            banner = Banner.objects.create(name=validated_data.get('name',None),tenent_user=user, multi_images=all_pictures)
            banner.save()
            return banner
    def to_representation(self, instance):
        context = super(BannerSerializer, self).to_representation(instance)
        multi_images = json.loads(context['multi_images'])
        return {
            "id":context["id"],
            'images':multi_images,
            'name':context['name']
        }
        
        


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class VendorMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("id","name", )
        read_only_fields=("name",)

class MaterialCreateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"

class MaterialRUDSerializer(WritableNestedModelSerializer):
    maker = VendorMaterialSerializer(required=False,)
    class Meta:
        model = Material
        fields = "__all__"



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



class VendorProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("name", )

class MaterialSerializer(serializers.ModelSerializer):
    # maker = VendorSerializer()
    class Meta:
        model=Material
        fields = ['id','name',]
class ProjectListSerializer(serializers.ModelSerializer):
    approver = ApproverSerializer()
    employee = ApproverSerializer(many=True)
    material = MaterialSerializer(many=True)
    class Meta:
        model = Project
        fields = "__all__"
class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
"""Project serializer ends"""

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


