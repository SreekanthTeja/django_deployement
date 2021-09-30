from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('token', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    # path('nu/create',UserCreateView.as_view(), name='user-create'),

    path('company/list/admin',CompanyListView.as_view()),
    path('company/create/admin',CompanyCreateView.as_view()),
    path('company/rud/<int:pk>',CompanyRUDView.as_view(), name='company-update'),

    path('plans',PlanListView.as_view()),
    path('plans/read/<int:pk>',PlanReadView.as_view()),

    path('payment/request', PaymentView.as_view()),
    path('payment/success', PaymentResponseView.as_view()),

    # path('emp/rud/<int:pk>', UserUpdateView.as_view()),
    path('password/<str:email>/reset',RestPasswordAPIView.as_view()),
    path('password/<str:email>/forgot',RestPasswordAPIView.as_view()),
    path('request/otp',OTPRequestAPIView.as_view()),
    path('verify/otp',OTPVerifyAPIView.as_view()),

    path('contact',ContactUsAPIView.as_view()),
    path('contact/create',ContactUsCreateAPIView.as_view()),
]