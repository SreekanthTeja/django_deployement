from django.shortcuts import render
from rest_framework import generics
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

class LicenseListCreateView(generics.ListCreateAPIView):
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
class UpdateLicenseView(generics.UpdateAPIView):
    queryset = License.objects.all()
    serializer_class = LicenseUpdateSerializer

class RDLicenseView(generics.RetrieveDestroyAPIView):
    queryset = License.objects.all()
    serializer_class = LicenseSingleInfoSerializer
    def delete(self, request, pk):
        licensee = self.queryset.get(id = pk)
        licensee.delete()
        user = User.objects.get(id = request.user.id)
        user.no_licenses -= 1
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT) 



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