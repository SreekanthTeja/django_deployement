from django.shortcuts import render
from rest_framework import generics
from rest_framework import views
from .api.serializers import *
from .models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
User = get_user_model()

"""
    User Registrtion for comapany
"""


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    
class RUDUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

"""License list api view """
class LicenseListAPIView(generics.ListAPIView):
    queryset = License.objects.all()
    serializer_class = LicenseListSerializer

"""License create api view """
class LicenseListCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = License.objects.all()
    serializer_class = LicenseCreateSerializer
    def perform_create(self, serializer):
        user= self.request.user
        print(user.no_licenses)
        try:
            user.no_licenses += 1
            user.save()
        except Exception(e):
            print(e)
        finally:
            serializer.save()

"""License update api view """
class UpdateLicenseView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = License.objects.all()
    serializer_class = LicenseUpdateSerializer

    
"""License  pecific read delete api view """
class RDLicenseView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = License.objects.all()
    serializer_class = LicenseSingleInfoSerializer
    def delete(self, request, pk):
        licensee = self.queryset.get(id = pk)
        licensee.delete()
        user = User.objects.get(id = request.user.id)
        user.no_licenses -= 1
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT) 

"""Device names list api view """
class DeviceListAPIView(generics.ListAPIView):
    queryset = DeviceName.objects.all()
    serializer_class = DeviceSerializer

"""Inspection Type  list api view """
class QSTypeListAPIView(views.APIView):
    def get(self, request):
        typee = QualityLibrary.TYPE
        d1 = [{"id":i[0],"name":i[1]} for i in typee]
        return Response(d1)


"""Quality list create api view """
class QualityListCreateAPIView(generics.ListCreateAPIView):
    queryset = QualityLibrary.objects.all()
    serializer_class = QualitySerializer

"""Quality read, update, delete api view """
class RUDQualityView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QualityLibrary.objects.all()
    serializer_class = QualitySerializer


"""Safety list create api view """
class SafetyListCreateAPIView(generics.ListCreateAPIView):
    queryset = SafetyLibrary.objects.all()
    serializer_class = SafetySerializer
"""Safety read, update, delete api view """
class RUDSafetyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SafetyLibrary.objects.all()
    serializer_class = SafetySerializer

"""Checklist list create"""
class CheckListCreateAPIView(generics.ListCreateAPIView):
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer
    
"""Checklist read, update, delete"""
class RUDCheckView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer

"""Banner list create"""
class BannerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    
"""Banner read, update, delete"""
class RUDBannerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

"""FAQ list create"""
class FAQListCreateAPIView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    
"""FAQ read, update, delete"""
class RUDFAQView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer