from django.urls import path
from .views import *
urlpatterns = [
    ########### user registration api's ##################
    path('list_or_create',RegistrationListCreateView.as_view()),
    path('rud/<int:pk>',RUDRegistrationView.as_view()),

    ########### user license api's ##################
    path('license/list_or_create',LicenseListCreateView.as_view()),
    path('license/update/<int:pk>',UpdateLicenseView.as_view()),
    path('license/user/<int:pk>', LicenseUserListView.as_view()),

    ########### quality assurence  api's ##################
    path('quality/list_or_create',QualityListCreateAPIView.as_view()),
    path('quality/rud/<int:pk>',RUDQualityView.as_view()),

    ########### quality check-list api's ##################
    path('quality/check/list_or_create',QualityCheckListCreateAPIView.as_view()),
    path('quality/check/rud/<int:pk>',RUDQualityCheckView.as_view()),

]