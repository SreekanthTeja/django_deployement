from rest_framework.permissions import BasePermission, IsAdminUser
from django.contrib.auth import get_user_model
User = get_user_model()

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.user_type==User.SUPER_ADMIN

class IsTenentUser(BasePermission):
    def has_permission(self, request, view):
        # print("......",request.user)
        return request.user.user_type==User.TENENT

class IsTenentOrUser(BasePermission):
    def has_permission(self, request, view):
        print("......",request.user)
        return  request.user.user_type=='TN' or request.user.user_type=='NU'