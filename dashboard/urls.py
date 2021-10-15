from django.urls import path, include
from dashboard.views import *
urlpatterns = [
    path('project/analysis',ProjectAnalyticsAPIView.as_view()),
    path('project/analysis/read/<int:pk>',ProjectDetailedAnalyticsAPIView.as_view()),
    path('checklists/usage',ChecklistUsageAPIView.as_view()),
    path('checklists/usage/by/project/<int:pk>',ChecklistUsageReadAPIView.as_view()),
]