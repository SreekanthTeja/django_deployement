from django.urls import path
from .views import *

urlpatterns = [
    path('company/list_or_create',CompanyListCreateView.as_view(), name='company-list-create'),
    path('company/rd/<int:pk>',CompanyRUDView.as_view(), name='company-rud'),
    path('company/update/<int:pk>',CompanyUpdateView.as_view(), name='company-update'),
]