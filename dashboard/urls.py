from django.urls import path, include
from dashboard.views import *
urlpatterns = [
    path('project/analysis',ProjectAnalyticsAPIView.as_view()),
    path('project/analysis/read/<int:pk>',ProjectDetailedAnalyticsAPIView.as_view()),
    path('project/checklists',ChecklistAnalyticsAPIView.as_view()),
]