from django.shortcuts import render
from rest_framework import generics, views, status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from bigspace.permissions import *
from buildcorn.models import Project
from dashboard.api.serializers import *

# Create your views here.
User = get_user_model()

class ProjectAnalyticsAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Project.objects.all()
    serializer_class = ProjectAnalyticSerializer
    def get_queryset(self):
        return self.queryset.filter(company__user=self.request.user)