from django.urls import path
from .views import *

urlpatterns = [
    ############# signup for normal users ################################
    path('user/superadmin',SuperAdminListView.as_view(), name='user-list'),

    # path('company/list_or_create',CompanyListCreateView.as_view(), name='company-list-create'),
    path('company/rud/<int:pk>',CompanyRUDView.as_view(), name='company-update'),

    path('plans',PlanListView.as_view()),
    path('payment/response', PaymentView.as_view()),
    path('payment/success', PaymentResponseView.as_view()),


    ############# signup for employee users ################################
    # path('company/emp/signup/<int:cid>',EmployeeSignup.as_view(), name='emp-signup'),
    # path('company/emp/list/<int:company_id>',EmployeeListAPIView.as_view(), name='emp-signup'),

    # path('contact/person',ContactPersonAPIView.as_view(), name='contact-person'),
]