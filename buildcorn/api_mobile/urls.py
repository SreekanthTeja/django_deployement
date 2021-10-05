from django.urls import path
from .views import *
urlpatterns = [
    path('project',ProjectListAPIView.as_view()),
    # path('project/download',DownloadProjectListAPIView.as_view()),
    path('project/inspection/<str:name>',InspectionAPIView.as_view()),
]