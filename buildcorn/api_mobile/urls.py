from django.urls import path
from .views import *
urlpatterns = [
    path('project',ProjectListAPIView.as_view()),
    path('project/read/<int:pk>',ProjectReadAPIView.as_view()),
    path('project/inspection/<str:name>',InspectionAPIView.as_view()),

    path('site/observation/list_or_create',SiteObservationAPIView.as_view()),
    path('site/observation/rud/<int:pk>',SiteObservationUpdateAPIView.as_view()),
    path('ncr/list_or_create',NCRAPIView.as_view()),
    path('ncr/rud/<int:pk>',NCR_RUDAPIView.as_view()),

    path('approver',ApproverAPIView.as_view()),
    path('approver/rud/<int:pk>',ApproverRUDAPIView.as_view()),
]