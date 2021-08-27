from django.shortcuts import render
from rest_framework import generics
from rest_framework import views
from .api.serializers import *
from .models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
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


class LicenseListAPIView(generics.ListAPIView):
    queryset = License.objects.all()
    serializer_class = LicenseListSerializer
class LicenseListCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = License.objects.all()
    serializer_class = LicenseCreateSerializer

    def perform_create(self, serializer):
        user= self.request.user
        print(user.no_licenses)
        try:
            user.no_licenses += 1
            user.save()
        except Exception(e):
            print(e)
        finally:
            serializer.save()
class UpdateLicenseView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = License.objects.all()
    serializer_class = LicenseUpdateSerializer
    

class RDLicenseView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = License.objects.all()
    serializer_class = LicenseSingleInfoSerializer
    def delete(self, request, pk):
        licensee = self.queryset.get(id = pk)
        licensee.delete()
        user = User.objects.get(id = request.user.id)
        user.no_licenses -= 1
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class DeviceListAPIView(generics.ListAPIView):
    queryset = DeviceName.objects.all()
    serializer_class = DeviceSerializer


class QSTypeListAPIView(views.APIView):
    def get(self, request):
        typee = QualityLibrary.TYPE
        d1 = {"id":[],"name":[]}
        l2 = [d1["id"].append(row[i]) if i == 0 else d1["name"].append(row[i]) for i in range(len(typee)) for row in typee]
        return Response(d1)
"""Quality"""

class QualityListCreateAPIView(generics.ListCreateAPIView):
    queryset = QualityLibrary.objects.all()
    serializer_class = QualitySerializer

class RUDQualityView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QualityLibrary.objects.all()
    serializer_class = QualitySerializer


"""Safety"""

class SafetyListCreateAPIView(generics.ListCreateAPIView):
    queryset = SafetyLibrary.objects.all()
    serializer_class = SafetySerializer

class RUDSafetyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SafetyLibrary.objects.all()
    serializer_class = SafetySerializer

"""Checklist """
class CheckListCreateAPIView(generics.ListCreateAPIView):
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer

class RUDCheckView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer