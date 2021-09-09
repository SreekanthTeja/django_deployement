from django.shortcuts import render, reverse
from rest_framework import generics
from rest_framework import views
from .serializers import *
from buildcorn.models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
User = get_user_model()


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        print("......",request.user)
        return User.SUPER_ADMIN==request.user.user_type

# """License list api view """
# class LicenseListAPIView(generics.ListAPIView):
#     queryset = License.objects.all()
#     serializer_class = LicenseListSerializer

# """License create api view """
# class LicenseListCreateView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = License.objects.all()
#     serializer_class = LicenseCreateSerializer
#     def perform_create(self, serializer):
#         user= self.request.user
#         print(user.no_licenses)
#         try:
#             user.no_licenses += 1
#             user.save()
#         except Exception(e):
#             print(e)
#         finally:
#             serializer.save()

# """License update api view """
# class UpdateLicenseView(generics.RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = License.objects.all()
#     serializer_class = LicenseUpdateSerializer

    
# """License  pecific read delete api view """
# class RDLicenseView(generics.RetrieveDestroyAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = License.objects.all()
#     serializer_class = LicenseSingleInfoSerializer
#     def delete(self, request, pk):
#         licensee = self.queryset.get(id = pk)
#         licensee.delete()
#         user = User.objects.get(id = request.user.id)
#         user.no_licenses -= 1
#         user.save()
#         return Response(status=status.HTTP_204_NO_CONTENT) 

# """Device names list api view """
# class DeviceListAPIView(generics.ListAPIView):
#     queryset = DeviceName.objects.all()
#     serializer_class = DeviceSerializer

"""License ApiView"""

class LicenseAPIView(generics.ListAPIView):
    permission_classes = (IsSuperUser,)
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    

"""Inspection Type  list api view """
class QSTypeListAPIView(views.APIView):
    def get(self, request):
        typee = QualityLibrary.TYPE
        d1 = [{"id":i[0],"name":i[1]} for i in typee]
        return Response(d1)



"""Projects adding and listing  """
class ProjectListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def perform_create(self, serializer):
        print(self.request.user)
        company = Company.objects.get(user__email=self.request.user)
        print(company)
        serializer.save(company=company)



"""Projects read, update, delete api view """
class RUDProjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectUsersView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def get_queryset(self):

        print(self.request.user)
        company = Company.objects.get(user__email=self.request.user)




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



"""Checklist list create for super_admin only"""
class CheckListCreateAPIView(generics.CreateAPIView):
    # permission_classes = (IsSuperUser,IsAuthenticated,)
    queryset = CheckList.objects.all()
    serializer_class = CheckListSerializer



class CheckListAPIView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
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



