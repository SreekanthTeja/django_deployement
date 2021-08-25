from django.shortcuts import render
from rest_framework import generics
from .api.serializers import *
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
class RUDRegistrationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


"""
    License
"""

class LicenseListCreateView(generics.ListCreateAPIView):
    queryset = License.objects.all()
    serializer_class = LicenseCreateSerializer
    
class LicenseUserListView(generics.RetrieveDestroyAPIView):
    queryset=License.objects.all()
    serializer_class=LicenseSingleInfoSerializer

class UpdateLicenseView(generics.UpdateAPIView):
    queryset = License.objects.all()
    serializer_class = LicenseCreateSerializer


"""Quality"""

class QualityListCreateAPIView(generics.ListCreateAPIView):
    queryset = QualityLibrary.objects.all()
    serializer_class = QualitySerializer

class RUDQualityView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QualityLibrary.objects.all()
    serializer_class = QualitySerializer


"""Quality Checklist """
class QualityCheckListCreateAPIView(generics.ListCreateAPIView):
    queryset = CheckList.objects.all()
    serializer_class = QualityCheckListSerializer

class RUDQualityCheckView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CheckList.objects.all()
    serializer_class = QualityCheckListSerializer