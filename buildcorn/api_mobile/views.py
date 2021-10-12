
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



class InspectionAPIView(views.APIView):
    permission_classes = (IsAuthenticated,IsTenentOrUser)
    queryset = AnswerChecklist.objects.all()
    def post(self, request, **kwargs):
        # input_data = {
        #     "project":"Logos",
        #     "type":"Safety",
        #     "question": [
        #         {
        #             "id": 20,
        #             "question": "Why safety",
        #             "status": "Complied",
        #             "reason": None

        #         }
        #     ]
        # }
        # filee = request.FILES.get('report', None)
        
        # pdf = pdf_file(filee) if filee != None else "empty"
        # validation
        input_data = request.data
        if not  input_data.get("project") :
            raise serializers.ValidationError({'error':"project is missing"})
        if  not  input_data.get("type") :
            raise serializers.ValidationError({'error':"type is missing"})
        if not  input_data.get("question"):
            raise serializers.ValidationError({'error':"question is missing"})
        if not request.data.get('report', None):
            raise serializers.ValidationError({'error':"report is missing"})
        """Previous working logic"""
        # if not request.FILES.get('report', None):
        #     raise serializers.ValidationError({'error':"report is missing"})
        # pdf = pdf_file(request.FILES.get('report'))
        # print(">>>>>>>>",pdf)
        """"""
        # report = json.dumps(request.data.get('report'))
        
        pdf = pdf_file(input_data.get('report'))
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
            
            report = generate_report(typee =input_data["type"],project=input_data["project"], checklist=kwargs['name'],submitted_by = self.request.user.first_name, pdf =pdf)
            return Response({'status':'Inspection submission done'},status=status.HTTP_200_OK)
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
                raise serializers.ValidationError({'error':e})
            report = generate_report(typee =input_data["type"],project=input_data["project"], checklist=kwargs['name'],submitted_by = self.request.user.first_name, pdf=pdf)
            return Response({'status':"Inspection submission done"},status=status.HTTP_200_OK)

class SiteObservationAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,IsTenentOrUser)
    queryset = SiteObservation.objects.all()
    serializer_class = SiteObservationSerailizer
    def perform_create(self, serializer):
        try:
            user = Employee.objects.get(user__email=self.request.user)
            serializer.save(user=user)
        except Exception as e:
            raise serializers.ValidationError({'error':e})

class SiteObservationUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,IsTenentOrUser)
    queryset = SiteObservation.objects.all()
    serializer_class = SiteObservationUpdateSerailizer
    # def perform_update(self, serializer):
    #     try:
    #         user = Employee.objects.get(user__email=self.request.user)
    #         serializer.save(user=user)
    #     except Exception as e:
    #         raise serializers.ValidationError({'error':e})


class NCRAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,IsTenentOrUser)
    queryset = NCR.objects.all()
    serializer_class = NCRSerailizer
    def perform_create(self, serializer):
        try:
            user = Employee.objects.get(user__email=self.request.user)
            serializer.save(user=user)
        except Exception as e:
            raise serializers.ValidationError({'error':e})

class NCR_RUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,IsTenentOrUser)
    queryset = NCR.objects.all()
    serializer_class = NCRUpdateSerailizer
