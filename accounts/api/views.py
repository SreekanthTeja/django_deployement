from django.shortcuts import render
from rest_framework import generics
from rest_framework import views
from .serializers import *
from accounts.models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
User = get_user_model()

"""
    User Registrtion for comapany
"""


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # def create(self, request):
    #     print("perform_create enterd",request.data)
    #     serializer = self.serializer_class(self.queryset, data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.user = User.objects.create_user(**request.data.pop("user"))
    #         # serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors)

    
class CompanyUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyUpdateSerializer
    
class CompanyRUDView(generics.RetrieveDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

