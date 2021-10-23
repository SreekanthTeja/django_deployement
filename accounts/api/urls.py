from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('token', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('user/superadmin',SuperAdminListView.as_view(), name='user-list'),
    path('company/list/admin',CompanyListView.as_view()),
    path('company/create/admin',CompanyCreateView.as_view()),
    path('company/rud/<int:pk>',CompanyRUDView.as_view(), name='company-update'),
    path('send/<int:phoneno>/',OTPSendAPIView.as_view()),
    path('plans',PlanListView.as_view()),
    path('payment/request', PaymentView.as_view()),
    path('payment/success', PaymentResponseView.as_view()),
]