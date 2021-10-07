from django.urls import path, include
from dashboard.views import *
urlpatterns = [
    path('project/analysis',ProjectAnalyticsAPIView.as_view()),
]