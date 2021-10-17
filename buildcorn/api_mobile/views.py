
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
    permission_classes = (IsAuthenticated, IsTenentOrUser)
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        return self.queryset.filter(employee__user=self.request.user)

class ProjectReadAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsTenentOrUser)
    queryset = Project.objects.all()
    serializer_class = ProjectReadSerializer

    def get_queryset(self):
        return self.queryset.filter(employee__user=self.request.user)


class InspectionAPIView(views.APIView):
    permission_classes = (IsAuthenticated, IsTenentOrUser)
    queryset = AnswerChecklist.objects.all()

    def post(self, request, **kwargs):
        """
        {
            "project":"Logos",
            "type":"Quality",
            "area":"Tower2",
            "material":{
                "id":5,
                "quantity_used":10,
                "units":"Kg",
                "maker":2
            },
            "question": [
                {
                    "id": 17,
                    "question": "Why cement not usd?",
                    "status": "Complied",
                    "reason": ""
                },
                
            ]
        }
        """
        input_data = request.data
        # validation
        if not input_data.get("project"):
            raise serializers.ValidationError({'error': "project is missing"})
        if not input_data.get("type"):
            raise serializers.ValidationError({'error': "type is missing"})
        if not input_data.get("question"):
            raise serializers.ValidationError({'error': "question is missing"})
        if not input_data.get("area"):
            raise serializers.ValidationError({'error': "area is missing"})
        if not input_data.get("material"):
            raise serializers.ValidationError({'error': "material is missing"})

        checklist_name = kwargs["name"]
        user = self.request.user
        try:
            emp = Employee.objects.get(user=user)
            # project = Project.objects.filter(company=emp.company,employee=emp.id,name=input_data["project"],vendors__id=input_data["vendor"],material__id=input_data["material"])
            project = Project.objects.get(
                company=emp.company, employee__user=user, name=input_data["project"])
            # print()
            material = project.material.get(id=input_data["material"]["id"])
            material.b_qty = input_data["material"]["quantity_used"]
            material.b_uom = input_data["material"]["units"]
            material.save()
        except Exception as e:
            raise serializers.ValidationError(
                {"error": "You dont have permissions for inspections"})

        # project.vendors
        if input_data["type"] == 'Quality':
            quality_checklist_name = QualityCheckList.objects.get(name__exact=kwargs['name'])
            try:
                for que in input_data.get('question'):
                    question = Question.objects.get(id=que["id"])
                    query, created = self.queryset.get_or_create(
                        project=project, question=question, quality_checklist=quality_checklist_name, area=input_data.get("area"), vendor=material.maker)
                    # query, created = self.queryset.get_or_create(project=project,question=question, quality_checklist=quality_checklist_name,)

                    if created:
                        query.status = que.get('status', None)
                        query.reason = que.get('reason', None)
                        query.save()
                        approver_action(input_data, user, checklist_name)
                    elif not created:
                        query.status = que.get('status', None)
                        query.reason = que.get('reason', None)
                        query.save()
                        approver_action(input_data, user, checklist_name)
            except Exception as e:
                raise serializers.ValidationError({'error': e})
            """Report generating logic"""
            # report = generate_report(typee =input_data["type"],project=input_data["project"], checklist=kwargs['name'],submitted_by = self.request.user.first_name, pdf =pdf)
            return Response({'status': 'Inspection submission done'}, status=status.HTTP_200_OK)
        else:
            try:
                safety_checklist_name = SafetyCheckList.objects.get(
                    name__exact=kwargs['name'])
                # project = Project.objects.get(name=input_data["project"])
                for que in input_data.get('question'):
                    question = Question.objects.get(id=que["id"])
                    query, created = self.queryset.get_or_create(project=project, question=question, safety_checklist=safety_checklist_name, area=input_data['area'], vendor=material.maker)
                    # query, created = self.queryset.get_or_create(project=project,question=question, safety_checklist=safety_checklist_name,)
                    print("{}=={}".format(query, created))
                    if created:
                        query.status = que.get('status', None)
                        query.reason = que.get('reason', None)
                        query.save()
                        approver_action(input_data, user, checklist_name)
                    elif not created:
                        query.status = que.get('status', None)
                        query.reason = que.get('reason', None)
                        query.save()
                        approver_action(input_data, user, checklist_name)
            except Exception as e:
                raise serializers.ValidationError({'error': e})
            """Report generating logic"""
            # report = generate_report(typee =input_data["type"],project=input_data["project"], checklist=kwargs['name'],submitted_by = self.request.user.first_name, pdf=pdf)
            return Response({'status': "Inspection submission done"}, status=status.HTTP_200_OK)


class SiteObservationAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsTenentOrUser)
    queryset = SiteObservation.objects.all()
    serializer_class = SiteObservationSerailizer

    def perform_create(self, serializer):
        try:
            user = Employee.objects.get(user__email=self.request.user)
            serializer.save(user=user)
        except Exception as e:
            raise serializers.ValidationError({'error': e})


class SiteObservationUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTenentOrUser)
    queryset = SiteObservation.objects.all()
    serializer_class = SiteObservationUpdateSerailizer
    # def perform_update(self, serializer):
    #     try:
    #         user = Employee.objects.get(user__email=self.request.user)
    #         serializer.save(user=user)
    #     except Exception as e:
    #         raise serializers.ValidationError({'error':e})


class NCRAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsTenentOrUser)
    queryset = NCR.objects.all()
    serializer_class = NCRSerailizer

    def perform_create(self, serializer):
        try:
            user = Employee.objects.get(user__email=self.request.user)
            serializer.save(user=user)
        except Exception as e:
            raise serializers.ValidationError({'error': e})


class NCR_RUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTenentOrUser)
    queryset = NCR.objects.all()
    serializer_class = NCRUpdateSerailizer


class ApproverAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsTenentOrUser)
    queryset = Approver.objects.all()
    serializer_class = ApproverSerializer

    def get_queryset(self):
        return self.queryset.filter(project__approver__user__email=self.request.user)


class ApproverRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTenentOrUser)
    queryset = Approver.objects.all()
    serializer_class = ApproverSerializer
    # def update(self, request, pk):
    #     return Response({"Approved successfully"}, status=status.HTTP_200_OK)
