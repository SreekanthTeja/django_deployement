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
        print("......",request.user)
        return User.SUPER_ADMIN==request.user.user_type



"""License ApiView"""

class LicenseAPIView(generics.ListAPIView):
    permission_classes = (IsSuperUser,)
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    

"""Employees"""

class EmployeeAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        if self.request.user.user_type == User.TENENT:
            emp = self.queryset.filter(company__user=self.request.user)
            return emp

class EmployeeCreateAPIView(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

"""Inspection Type  list api view """
class QSTypeListAPIView(views.APIView):
    def get(self, request):
        typee = QualityLibrary.TYPE
        d1 = [{"id":i[0],"name":i[1]} for i in typee]
        return Response(d1)



"""Projects adding and listing  """
class ProjectListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def perform_create(self, serializer):
        print(self.request.user)
        company = Company.objects.get(user__email=self.request.user)
        print(company)
        serializer.save(company=company)



"""Projects read, update, delete api view """
class RUDProjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectUsersView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def get_queryset(self):

        print(self.request.user)
        company = Company.objects.get(user__email=self.request.user)




"""Quality list create api view """
class QualityListCreateAPIView(generics.ListCreateAPIView):
    queryset = QualityLibrary.objects.all()
    serializer_class = QualitySerializer

"""Quality read, update, delete api view """
class RUDQualityView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QualityLibrary.objects.all()
    serializer_class = QualitySerializer


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
    # permission_classes = (IsSuperUser,IsAuthenticated,)
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer




class CheckListAPIView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer
"""Checklist read, update, delete"""
class RUDCheckView(generics.RetrieveUpdateDestroyAPIView):
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



