from django.urls import path
from .views import *
from .checklist_views import *
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

    ###########  admin safety url's ##################

    path('safety/check/list',AdminSafetyListView.as_view()),
    path('safety/check/create',SafetyCreateView.as_view()),
    path('safety/check/rd/<int:pk>',RDSafetyView.as_view()),
    path('safety/check/update/<int:pk>',UpdateSafetyView.as_view()),
    ###########  admin quality url's ##################

    path('quality/check/list',AdminQualityListView.as_view()),
    path('quality/check/create',QualityCreateiew.as_view()),
    path('quality/check/rd/<int:pk>',RDQualitylView.as_view()),
    path('quality/check/update/<int:pk>',UpdateQualitylView.as_view()),
    # path('safety/check/list',SafetyCheckListAPIView.as_view()),
    # path('check/create',CheckListCreateAPIView.as_view()),
    # path('check/rd/<int:pk>',RDCheckView.as_view()),
    # path('check/update/<int:pk>',UpdateCheckView.as_view()),

    # ########### admin questions  url's ##################
    path('question/list',QuestionListView.as_view()),
    path('question/create',QuestionCreateView.as_view()),
    path('question/rud/<int:pk>',RUDQuestionlView.as_view()),

    # ########### quality  url's ##################


    path('quality/checklist/assign/project',QualityAssignProjectAPIView.as_view()),
    path('safety/checklist/assign/project',SafetyAssignProjectAPIView.as_view()),
    path('quality/project',ShowQualityProjectView.as_view()),
    path('safety/project',ShowSafetyProjectView.as_view()),

    path('faq/list_or_create',FaqLCView.as_view()),
    path('faq/rud/<int:pk>',RUDFaqView.as_view()),

    path('material/list_or_create',MaterialLCView.as_view()),
    path('material/rud/<int:pk>',RUDMaterialView.as_view()),

    path('vendor/list_or_create',VendorLCView.as_view()),
    path('vendor/rud/<int:pk>',RUDVendorlView.as_view()),
]


