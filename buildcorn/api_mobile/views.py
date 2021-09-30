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
import json
# import pandas as pd
User = get_user_model()


class ProjectListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsTenentOrUser)
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    def get_queryset(self):
        return self.queryset.filter(employee__user=self.request.user)

# class DownloadProjectListAPIView(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,IsTenentOrUser)
#     queryset = Project.objects.all()
#     serializer_class = ProjectListSerializer
#     def get_queryset(self):
#         return self.queryset.filter(employee__user=self.request.user)

#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = ProjectListSerializer(queryset, many=True)
#         j_data = json.dumps(serializer.data)
#         j_data = json.loads(j_data)
#         print(j_data[0])
#         return Response(serializer.data)

# class InspectionSafetyAPIView(generics.UpdateAPIView):
#     queryset = Question.objects.all()
#     pass
class InspectionQualityView(generics.RetrieveUpdateAPIView):
    queryset = QualityCheckList.objects.all()
    serializer_class = InspectionQualitySerializer
    lookup_field = "name"


