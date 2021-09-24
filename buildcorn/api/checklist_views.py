from django.shortcuts import render, reverse
from rest_framework import generics
from rest_framework import views
# from .serializers import *
from .checklists_serializers import *
from buildcorn.models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from bigspace.permissions import *
import datetime

User = get_user_model()


class SafetyListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsSuperUser, IsTenentUser)
    queryset = SafetyCheckList.objects.all()
    serializer_class = SafetySerializer
    # def get_queryset(self):
    #     return self.queryset.filter(question__typee=Question.Safety)

class SafetyCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    queryset = SafetyCheckList.objects.all()
    serializer_class = SafetySerializer

class RUDSafetyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = SafetyCheckList.objects.all()
    serializer_class = SafetySerializer


class QualityListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsSuperUser, IsTenentUser)
    queryset = QualityCheckList.objects.all()
    serializer_class = QualitySerializer
    # def get_queryset(self):
    #     return self.queryset.filter(question__typee=Question.Quality)



class QualityCreateiew(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,IsSuperUser)
    queryset = QualityCheckList.objects.all()
    serializer_class = QualitySerializer


class RUDQualitylView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = QualityCheckList.objects.all()
    serializer_class = QualitySerializer


class QuestionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsSuperUser, IsTenentUser)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,IsSuperUser)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class RUDQuestionlView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer