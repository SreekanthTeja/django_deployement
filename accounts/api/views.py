from django.shortcuts import render
from rest_framework import generics
from rest_framework import views
from .serializers import *
from accounts.models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

User = get_user_model()



# class IsSuperUser(IsAdminUser):
#     def has_permission(self, request, view):
#         print("......",request.user)
#         return User.SUPER_ADMIN==request.user.user_type
"""
    User apis for comapany
"""
class SuperAdminListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(user_type=User.SUPER_ADMIN)
    


"""
    Company apis 
"""
class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    def perform_create(self, serializer):
        User.user_type = User.TENENT
        serializer.save()


class CompanyRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyUpdateSerializer
    def update(self, request, *args, **kwargs):
        data = request.data
        try:
            if data["user"]["id"]:
                user_instance = User.objects.get(id= data["user"]["id"])
                if "email" in data["user"]:
                    user_instance.email = data["user"]["email"]
                if "first_name" in data["user"]:
                    user_instance.first_name = data["user"]["first_name"]
                if "phone_number" in data["user"]:
                    user_instance.first_name = data["user"]["phone_number"]
                user_instance.save()

        except Exception as e:
            return Response({"status":"user object id required"})
        
        company_instance = self.get_object()
        try:

            if "user" in data :
                company_instance.user = user_instance
            if "name" in data :
                company_instance.name= data["name"]
            if "gstin" in data :
                company_instance.gstin= data["gstin"]
            if "state" in data :
                company_instance.state= data["state"]
            if "city" in data :
                company_instance.state= data["city"]
            if "pincode" in data :
                company_instance.state= data["pincode"]
            if "addres" in data :
                company_instance.state= data["addres"]
            company_instance.save()
            return Response({'status':"Updated"})
        except Exception as e:
            pass
            
    

    
class CompanyRDView(generics.RetrieveDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class EmployeeSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, **kwargs):
        cid = kwargs["cid"]
        user = User.objects.create_user(**request.data)
        company = Company.objects.filter(company_id= cid)
        print(company)
        company[0].employees.add(user.id)
        return Response({"status":"Successfull registerd"})
class EmployeeListAPIView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyEmployeeListSerializer
    lookup_field = "company_id"
    
class ContactPersonAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ContactPersonSerializer

    def get_queryset(self):
        user = self.queryset.filter(user_type=User.SUPER_ADMIN)
        return user




