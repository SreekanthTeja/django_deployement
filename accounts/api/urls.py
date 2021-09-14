from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    # path('login', UserLoginAPIView.as_view()),
    path('token', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('user/superadmin',SuperAdminListView.as_view(), name='user-list'),
    path('company/list/admin',CompanyListView.as_view()),
    path('company/create/admin',CompanyCreateView.as_view()),
    path('company/rud/<int:pk>',CompanyRUDView.as_view(), name='company-update'),

    path('plans',PlanListView.as_view()),
    path('payment/request', PaymentView.as_view()),
    path('payment/success', PaymentResponseView.as_view()),



    ############# signup for employee users ################################
    # path('company/emp/signup/<int:cid>',EmployeeSignup.as_view(), name='emp-signup'),
    # path('company/emp/list/<int:company_id>',EmployeeListAPIView.as_view(), name='emp-signup'),

    # path('contact/person',ContactPersonAPIView.as_view(), name='contact-person'),
]