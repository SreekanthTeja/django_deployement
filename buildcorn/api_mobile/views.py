from rest_framework import generics
from rest_framework import views
# from buildcorn.api.serializers import *
from buildcorn.api_mobile.serializers import *
from buildcorn.models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from bigspace.permissions import *

User = get_user_model()


# class ProjectListAPIView(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,IsTenentOrUser)
#     queryset = Project.objects.all()
#     serializer_class = ProjectListSerializer
#     def get_queryset(self):
#         print(self.request.user)
#         q = self.queryset.filter(employee__user=self.request.user)
#         print('>>>>>',q)
#         return q