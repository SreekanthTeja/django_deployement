from django.urls import path
from .views import *
urlpatterns = [
    ###########  license url's ##################
    path('license', LicenseAPIView.as_view()),

    ########### project  url's ##################
    path('project/create',ProjectCreateAPIView.as_view()),
    path('project/list',ProjectListAPIView.as_view()),
    path('project/rd/<int:pk>',RUDProjectView.as_view()),
    path('project/update/<int:pk>', ProjectUpdateView.as_view()),

    ###########  employee url's ##################
    path('emp/list_or_create', EmployeeAPIView.as_view()),
    path('emp/rud/<int:pk>', EmpRUDView.as_view()),

    # ########### checklists   url's ##################
    # path('checklist/create',ChecklistCreateAPIView.as_view()),
    # path('checklist/list',CheckListAPIView.as_view()),
    # path('checklist/rud/<int:pk>',RUDChecklistView.as_view()),
    # path('checklist/checklist/<int:pk>',ChecklistCheckListView.as_view()),

    ########### safety assurence  url's ##################
    # path('safety/create',SafetyCreateAPIView.as_view()),
    # path('safety/list',SafetyListAPIView.as_view()),
    # path('safety/rud/<int:pk>',RUDSafetyView.as_view()),
    # path('safety/checklist/<int:pk>',SafetyCheckListView.as_view()),

    ###########  check-list url's ##################

    path('quality/check/list',QualityCheckListAPIView.as_view()),
    path('safety/check/list',SafetyCheckListAPIView.as_view()),
    path('check/create',CheckListCreateAPIView.as_view()),
    path('check/rd/<int:pk>',RDCheckView.as_view()),
    path('check/update/<int:pk>',UpdateCheckView.as_view()),

    # ########### banner  url's ##################
    path('question/create',QuestionView.as_view()),
    path('question/rud/<int:pk>',RUDQuestionView.as_view()),

    # ########### quality  url's ##################
    path('quality/checklist/assign/project',QualityAssignChecklistAPIView.as_view()),
    path('safety/checklist/assign/project',SafetyAssignChecklistAPIView.as_view()),
    path('quality/project',QualityShowProjectAssign.as_view()),
    path('safety/project',SafetyShowProjectAssign.as_view()),

    path('faq/list_or_create',FaqLCView.as_view()),
    path('faq/rud/<int:pk>',RUDFaqView.as_view()),


]


