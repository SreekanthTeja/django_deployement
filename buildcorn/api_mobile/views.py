
from rest_framework import views, generics, serializers, status
from buildcorn.api_mobile.serializers import *
from buildcorn.models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response

from bigspace.permissions import *
import json
from .utils import *
User = get_user_model()


class ProjectListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsTenentOrUser)
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    def get_queryset(self):
        return self.queryset.filter(employee__user=self.request.user)


# class InspectionSafetyAPIView(generics.UpdateAPIView):
    # permission_classes = (IsAuthenticated,IsTenentOrUser)
    # serializer_class = InspectionQualitySerializer
    # lookup_field = "quality_checklist__name"
class InspectionAPIView(views.APIView):
    permission_classes = (IsAuthenticated,IsTenentOrUser)
    queryset = AnswerChecklist.objects.all()
    def post(self, request, **kwargs):
        input_data = request.data
        # print(input_data)
        if input_data["type"] == 'Quality':
            project = Project.objects.get(name=input_data["project"])
            quality_checklist_name = QualityCheckList.objects.get(name__exact=kwargs['name'])
            try:
                for que in input_data.get('question'):
                    question = Question.objects.get(id=que["id"])
                    query, created = self.queryset.get_or_create(project=project,question=question, quality_checklist=quality_checklist_name)
                    if created:
                        query.status = que.get('status',None)
                        query.reason =  que.get('reason',None)
                        query.save()
                    elif  not created:
                        query.status = que.get('status',None)
                        query.reason =  que.get('reason',None)
                        query.save()
            except Exception as e:
                raise serializers.ValidationError({'error':e}, status=status.HTTP_400_BAD_REQUEST)
            
            report = generate_report(typee =input_data["type"],project=input_data["project"], checklist=kwargs['name'],submitted_by = self.request.user.first_name)
            return Response({'status':'Success'},status=status.HTTP_200_OK)
        else:
            try:
                safety_checklist_name = SafetyCheckList.objects.get(name__exact=kwargs['name'])
                project = Project.objects.get(name=input_data["project"])
                for que in input_data.get('question'):
                    question = Question.objects.get(id=que["id"])
                    query, created = self.queryset.get_or_create(project=project,question=question, safety_checklist=safety_checklist_name)
                    if created:
                        query.status = que.get('status',None)
                        query.reason =  que.get('reason',None)
                        query.save()
                    elif not created:
                        query.status = que.get('status',None)
                        query.reason =  que.get('reason',None)
                        query.save()
            except Exception as e:
                raise serializers.ValidationError({'error':e}, status=status.HTTP_400_BAD_REQUEST)
            report = generate_report(typee =input_data["type"],project=input_data["project"], checklist=kwargs['name'],submitted_by = self.request.user.first_name)
            return Response({'status':"Success"},status=status.HTTP_200_OK)


    


