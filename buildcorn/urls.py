from django.urls import path
from .views import *
urlpatterns = [
    ########### user registration api's ##################
    path('list_or_create',UserListCreateView.as_view()),
    path('rud/<int:pk>',RUDUserView.as_view()),

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
    path('check/list',CheckListAPIView.as_view()),
    path('check/rud/<int:pk>',RUDCheckView.as_view()),

    ########### quality assurence  api's ##################
    path('quality/list_or_create',QualityListCreateAPIView.as_view()),
    path('quality/rud/<int:pk>',RUDQualityView.as_view()),

    ########### safety assurence  api's ##################
    path('safety/list_or_create',SafetyListCreateAPIView.as_view()),
    path('safety/rud/<int:pk>',RUDSafetyView.as_view()),

    ########### banner  api's ##################
    path('banner/list_or_create',BannerListCreateAPIView.as_view()),
    path('banner/rud/<int:pk>',RUDBannerView.as_view()),

    ########### faq  api's ##################
    path('faq/list_or_create',FAQListCreateAPIView.as_view()),
    path('faq/rud/<int:pk>',RUDFAQView.as_view()),

    ########### forms  urls ##################
    path('ui/check/list',CheckListFormView.as_view(), name='checklist-list'),
    path('ui/check/create',CheckListFCreateFormView.as_view(), name='checklist-create'),
    path('ui/check/detail/<int:pk>',ChecklistDetailView.as_view(), name='checklist-detail'),
]