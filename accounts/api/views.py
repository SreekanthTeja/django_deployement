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
    User apis for comapany
"""
class UserCreateListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class RUUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

"""
    Company apis 
"""
class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    def perform_create(self, serializer):
        User.user_type = User.TENENT 
        User.is_active = False
        serializer.save()
class CompanyUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyUpdateSerializer
    
class CompanyRDView(generics.RetrieveDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class EmployeeSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, **kwargs):
        cid = kwargs["cid"]
        user = User.objects.create_user(**request.data)
        company = Company.objects.filter(company_id= cid)
        print(company)
        company[0].employees.add(user.id)
        return Response({"status":"Successfull registerd"})
class EmployeeListAPIView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyEmployeeListSerializer
    lookup_field = "company_id"
    
class ContactPersonAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ContactPersonSerializer

    def get_queryset(self):
        user = self.queryset.filter(user_type=User.SUPER_ADMIN)
        return user




