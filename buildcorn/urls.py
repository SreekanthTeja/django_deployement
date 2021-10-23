from django.urls import path, include
from .views import *
urlpatterns = [
    
    ########### api  urls ##################
    path('api/',include("buildcorn.api.urls")),
    ########### forms  urls ##################
    path('ui/check/list',CheckListFormView.as_view(), name='checklist-list'),
    path('ui/check/create',CheckListFCreateFormView.as_view(), name='checklist-create'),
    path('ui/check/detail/<int:pk>',ChecklistDetailView.as_view(), name='checklist-detail'),
]