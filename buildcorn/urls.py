from django.urls import path
from .views import *
urlpatterns = [
    ########### user registration api's ##################
    path('list_or_create',RegistrationListCreateView.as_view()),
    path('rud/<int:pk>',RUDRegistrationView.as_view()),

    ########### user license api's ##################
    path('license/list',LicenseListAPIView.as_view()),
    path('license/create',LicenseListCreateView.as_view()),
    path('license/update/<int:pk>',UpdateLicenseView.as_view()),
    path('license/rd/<int:pk>', RDLicenseView.as_view()),


    ###########  quality safety type list view  ##################
    path('type/list',QSTypeListAPIView.as_view()),
    ###########  check-list api's ##################
    path('device/list',DeviceListAPIView.as_view()),

    ###########  check-list api's ##################
    path('check/list_or_create',CheckListCreateAPIView.as_view()),
    path('check/rud/<int:pk>',RUDCheckView.as_view()),

    ########### quality assurence  api's ##################
    path('quality/list_or_create',QualityListCreateAPIView.as_view()),
    path('quality/rud/<int:pk>',RUDQualityView.as_view()),

    ########### safety assurence  api's ##################
    path('safety/list_or_create',SafetyListCreateAPIView.as_view()),
    path('safety/rud/<int:pk>',RUDSafetyView.as_view()),
]