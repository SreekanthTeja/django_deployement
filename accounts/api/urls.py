from django.urls import path
from .views import *

urlpatterns = [
    path('users/list',UserListView.as_view(), name='user-list'),
    path('user/ru/<int:pk>',RUUserView.as_view(), name='user-read_update'),

    path('company/list_or_create',CompanyListCreateView.as_view(), name='company-list-create'),
    path('company/rd/<int:pk>',CompanyRUDView.as_view(), name='company-rud'),
    path('company/update/<int:pk>',CompanyUpdateView.as_view(), name='company-update'),
]