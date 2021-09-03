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
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.exclude(user_type='TN')
    
class RUUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

"""
    Company apis 
"""
class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
class CompanyUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyUpdateSerializer
    
class CompanyRDView(generics.RetrieveDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

