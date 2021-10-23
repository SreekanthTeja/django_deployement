from django.urls import path
from .views import *
urlpatterns = [
   

    path('type/list',QSTypeListAPIView.as_view()),
    ###########  license url's ##################
    path('license', LicenseAPIView.as_view()),

    ###########  employee url's ##################
    path('emp', EmployeeAPIView.as_view()),
    path('emp/create', EmployeeCreateAPIView.as_view()),
    path('emp/update/<int:pk>', EmployeeUpdateView.as_view()),
    path('emp/rd/<int:pk>', RDEmployeeAPIView.as_view()),


    ###########  check-list url's ##################
    path('check/create',CheckListCreateAPIView.as_view()),
    path('check/list',CheckListAPIView.as_view()),
    path('check/rud/<int:pk>',RUDCheckView.as_view()),

    ########### quality assurence  url's ##################
    path('quality/create',QualityCreateAPIView.as_view()),
    path('quality/list',QualityListAPIView.as_view()),
    path('quality/rud/<int:pk>',RUDQualityView.as_view()),
    path('quality/checklist/<int:pk>',QualityCheckListView.as_view()),

    ########### safety assurence  url's ##################
    path('safety/list_or_create',SafetyListCreateAPIView.as_view()),
    path('safety/rud/<int:pk>',RUDSafetyView.as_view()),

    ########### banner  url's ##################
    path('banner/list_or_create',BannerListCreateAPIView.as_view()),
    path('banner/rud/<int:pk>',RUDBannerView.as_view()),

    ########### faq  url's ##################
    path('faq/list_or_create',FAQListCreateAPIView.as_view()),
    path('faq/rud/<int:pk>',RUDFAQView.as_view()),

    ########### project  url's ##################
    path('project/create',ProjectCreateAPIView.as_view()),
    path('project/list',ProjectListAPIView.as_view()),
    path('project/rd/<int:pk>',RUDProjectView.as_view()),
    path('project/update/<int:pk>', ProjectUpdateView.as_view())
]

