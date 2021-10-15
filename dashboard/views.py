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

class ProjectDetailedAnalyticsAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Project.objects.all()
    serializer_class = ProjectAnalyticDetailSerializer
    # lookup_field = ""
    def get_queryset(self):
        return self.queryset.filter(company__user=self.request.user)


# class ChecklistAnalyticsAPIView(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,IsTenentUser)
#     queryset = Project.objects.all()
#     # serializer_class = ChecklistsAnalyticsSerializer
#     def get_queryset(self):
#         return self.queryset.filter(company__user=self.request.user)

#     def list(self, request):
#         all_checklist = [list(project.quality_checklist.values("name")) + list(project.safety_checklist.values("name")) for project in self.queryset.all()]
#         flat_list = [item for sublist in all_checklist for item in sublist]
#         result = {}
#         for checklist in flat_list:
#             if checklist["name"] not in result:
#                 result[checklist.get("name")] =0
#             result[checklist["name"]] +=1 
#         return Response(result, status=status.HTTP_200_OK)

class ChecklistUsageAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = ChecklistsUsage.objects.all()
    serializer_class = ChecklistsUsageSerializer
    def get_queryset(self):
        return self.queryset.filter(company__user__email=self.request.user)
class ChecklistUsageReadAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = ChecklistsUsage.objects.all()
    serializer_class = ChecklistsUsageSerializer
