from django.shortcuts import render, reverse
from rest_framework import generics
from rest_framework import views
from .serializers import *
from buildcorn.models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
User = get_user_model()


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        # print("......",request.user)
        return User.SUPER_ADMIN==request.user.user_type

class IsTenentUser(IsAdminUser):
    def has_permission(self, request, view):
        # print("......",request.user)
        return User.TENENT==request.user.user_type


"""License ApiView"""

class LicenseAPIView(generics.ListAPIView):
    permission_classes = (IsSuperUser,)
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    

"""Employees start"""

class EmployeeAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        if self.request.user.user_type == User.TENENT:
            emp = self.queryset.filter(company__user=self.request.user)
            return emp

class EmployeeCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer

class RDEmployeeAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        if self.request.user.user_type == User.TENENT:
            emp = self.queryset.filter(company__user=self.request.user)
            return emp

class EmployeeUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Employee.objects.all()
    serializer_class = EmployeeUpdateSerializer
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
"""Employees ends"""

"""Inspection Type  list api view """
class QSTypeListAPIView(views.APIView):
    def get(self, request):
        typee = QualityLibrary.TYPE
        d1 = [{"id":i[0],"name":i[1]} for i in typee]
        return Response(d1)



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





"""Quality list create api view """
class QualityCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = QualityLibrary.objects.all()
    serializer_class = QualityCreateSerializer

class QualityListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = QualityLibrary.objects.all()
    serializer_class = QualityListSerializer
"""Quality read, update, delete api view """
class RUDQualityView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = QualityLibrary.objects.all()
    serializer_class = RUDQualitySerializer
class QualityCheckListView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = QualityLibrary.objects.all()
    serializer_class = QualityCheckListSerializer

"""Safety list create api view """
class SafetyListCreateAPIView(generics.ListCreateAPIView):
    queryset = SafetyLibrary.objects.all()
    serializer_class = SafetySerializer
"""Safety read, update, delete api view """
class RUDSafetyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SafetyLibrary.objects.all()
    serializer_class = SafetySerializer



"""Checklist list create for super_admin only"""
class CheckListCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer




class CheckListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer
"""Checklist read, update, delete"""
class RUDCheckView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer

"""Banner list create"""
class BannerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    
"""Banner read, update, delete"""
class RUDBannerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

"""FAQ list create"""
class FAQListCreateAPIView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    
"""FAQ read, update, delete"""
class RUDFAQView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer



