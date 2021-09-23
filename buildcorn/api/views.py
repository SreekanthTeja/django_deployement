from django.shortcuts import render, reverse
from rest_framework import generics
from rest_framework import views
from .serializers import *
from buildcorn.models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from bigspace.permissions import *
import datetime

User = get_user_model()


"""License ApiView"""

class LicenseAPIView(generics.ListAPIView):
    permission_classes = (IsSuperUser,)
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    

"""Normal user view start"""

class EmployeeAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        print(self.request.user)
        if self.request.user.user_type == User.TENENT:
            return self.queryset.filter(company__user=self.request.user)
    def perform_create(self, serializer):
        comp = Company.objects.get(user__email=self.request.user)
        if comp.license_purchased == 0:
            raise serializers.ValidationError({'status':'Sorry  License wallet 0'})
        comp.license_purchased -= 1
        comp.save()
        serializer.save(company=comp)

    
class EmpRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,IsTenentOrUser)
    queryset = User.objects.all()
    serializer_class = EmployeeUserSerializer
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
    # def delete(self, request, pk):
    #     emp = Employee.objects.get(id=pk)
    #     if emp.user.email:
    #         print(True)
    #         user = User.objects.get(email=emp.user.email).delete()

    #         return Response({'status':'Deleted'})
    #     return Response({'status':'Unable to delete'})

"""Employees ends"""


"""Projects Starts """
class ProjectCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    def perform_create(self, serializer):
        print(self.request.user)
        company = Company.objects.get(user__email=self.request.user)
        print(company)
        serializer.save(company=company)

class ProjectListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    def get_queryset(self):
        print(self.request.user)
        q = self.queryset.filter(company__user=self.request.user)
        print('>>>>>',q)
        return q
"""Projects read, delete api view """
class RUDProjectView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

class ProjectUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
"""Projects Ends """

"""Checklist list create for super_admin only"""
class QualityCheckListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer
    def get_queryset(self):
        return CheckList.objects.filter(typee=CheckList.Quality).order_by("-id")

class SafetyCheckListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer
    def get_queryset(self):
        return CheckList.objects.filter(typee=CheckList.Safety)
"""Checklist Create"""
class CheckListCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,IsSuperUser)
    queryset = CheckList.objects.all()
    serializer_class = CheckListCreateSerializer

"""Checklist update"""
class UpdateCheckView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,IsSuperUser)
    queryset = CheckList.objects.all()
    serializer_class = CheckListUpdateSerializer

"""Checklist read, delete"""
class RDCheckView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer

"""Questions views"""
class QuestionView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,IsSuperUser,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    

class RUDQuestionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer



class QualityAssignChecklistAPIView(views.APIView):
    permission_classes = (IsAuthenticated,IsTenentUser,)
    def post(self, request):
        data = request.data
        check = data.get('checklists')
        try:
            project = Project.objects.get(id=data.get('project'))
            checklists = CheckList.objects.filter(id__in=check)
        except Exception as e:
            raise serializers.ValidationError({'status':e})
        project.checklists.set([i.id for i in checklists])
        date = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
        print(date)
        project.save()
        return Response({'status':"Assignment successfully done",'date':date})

class SafetyAssignChecklistAPIView(views.APIView):
    permission_classes = (IsAuthenticated,IsTenentUser,)
    def post(self, request):
        data = request.data
        check = data.get('checklists')
        try:
            project = Project.objects.get(id=data.get('project'))
            checklists = CheckList.objects.filter(id__in=check)
        except Exception as e:
            raise serializers.ValidationError({'status':e})
        project.checklists.set([i.id for i in checklists])
        project.save()
        return Response({'status':"Assignment successfully done"})



class  QualityShowProjectAssign(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser,)
    queryset = Project.objects.all()
    serializer_class = ProjectAssignSerializer
    def get_queryset(self):
        return self.queryset.filter(checklists__typee=CheckList.Quality).distinct()
    

class  SafetyShowProjectAssign(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser,)
    queryset = Project.objects.all()
    serializer_class = ProjectAssignSerializer
    def get_queryset(self):
        return self.queryset.filter(checklists__typee=CheckList.Safety).distinct()



class FaqLCView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer
    

class RUDFaqView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer