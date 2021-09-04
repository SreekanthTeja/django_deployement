from django.urls import path
from .views import *

urlpatterns = [
    ############# signup for normal users ################################
    path('user/list_or_signup',UserCreateListView.as_view(), name='user-list'),
    path('user/ru/<int:pk>',RUUserView.as_view(), name='user-read_update'),

    path('company/list_or_create',CompanyListCreateView.as_view(), name='company-list-create'),
    path('company/rd/<int:pk>',CompanyRDView.as_view(), name='company-rd'),
    path('company/update/<int:pk>',CompanyUpdateView.as_view(), name='company-update'),

    ############# signup for employee users ################################
    path('company/emp/signup/<int:cid>',EmployeeSignup.as_view(), name='emp-signup'),
    path('company/emp/list/<int:company_id>',EmployeeListAPIView.as_view(), name='emp-signup'),

    path('contact/person',ContactPersonAPIView.as_view(), name='contact-person'),
]