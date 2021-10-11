from django.shortcuts import render, reverse
from rest_framework import generics
from rest_framework import views
from .serializers import *
from .checklists_serializers import *
from buildcorn.models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from bigspace.permissions import *
import datetime
from django.db.models import Q
User = get_user_model()


"""License ApiView"""


class LicenseAPIView(generics.ListAPIView):
    permission_classes = (IsSuperUser,)
    queryset = License.objects.all()
    serializer_class = LicenseSerializer

class LicenseEmployeeAPIView(generics.ListAPIView):
    permission_classes = (IsSuperUser,)
    queryset = License.objects.all()
    serializer_class = LicenseEmployeeSerializer
    def get_queryset(self):
        return self.queryset.filter(Q(company__name=self.kwargs['company']) | Q(company__company_id=self.kwargs['company']))

"""Normal user view start"""


class EmployeeAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        print(self.request.user)
        if self.request.user.user_type == User.TENENT:
            return self.queryset.filter(company__user=self.request.user)

    def perform_create(self, serializer):
        comp = Company.objects.get(user__email=self.request.user)
        if comp.license_purchased == 0:
            raise serializers.ValidationError(
                {'status': 'Sorry  License wallet 0'})
        # comp.license_purchased -= 1
        comp.save()
        serializer.save(company=comp)


class EmpRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTenentOrUser)
    queryset = User.objects.all()
    serializer_class = EmployeeUserSerializer
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
    # def delete(self, request, pk):
    #     emp = Employee.objects.get(id=pk)
    #     if emp.user.email:
    #         print(True)
    #         user = User.objects.get(email=emp.user.email).delete()

    #         return Response({'status':'Deleted'})
    #     return Response({'status':'Unable to delete'})


"""Employees ends"""


"""Projects Starts """


class ProjectCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        company = Company.objects.get(user__email=self.request.user)
        print(company)
        serializer.save(company=company)


class ProjectListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        print(self.request.user)
        q = self.queryset.filter(company__user=self.request.user)
        print('>>>>>', q)
        return q


"""Projects read, delete api view """


class RUDProjectView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer


class ProjectUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


"""Projects Ends """

class QualityAssignProjectAPIView(views.APIView):
    permission_classes = (IsAuthenticated, IsTenentUser,)

    def post(self, request):
        data = request.data
        check = data.get('quality')
        if Project.objects.filter(id=data.get('project')).exists() and QualityCheckList.objects.filter(id__in=check).exists():

            project = Project.objects.get(id=data.get('project'))
            checklists = QualityCheckList.objects.filter(id__in=check)
            project.quality_checklist.set([i.id for i in checklists])
            date = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
            project.save()
            return Response({'status': "Assignment successfully done", 'date': date})
        
        raise serializers.ValidationError({'error': 'Unsupported checklists'})


class SafetyAssignProjectAPIView(views.APIView):
    permission_classes = (IsAuthenticated, IsTenentUser,)

    def post(self, request):
        data = request.data
        check = data.get('safety')
        if Project.objects.filter(id=data.get('project')).exists() and SafetyCheckList.objects.filter(id__in=check).exists():
            project = Project.objects.get(id=data.get('project'))
            checklists = SafetyCheckList.objects.filter(id__in=check)
            project.safety_checklist.set([i.id for i in checklists])
            date = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
            project.save()
            return Response({'status': "Assignment successfully done", 'date': date})
        raise serializers.ValidationError({'error': 'Unsupported checklists'})


class ShowQualityProjectView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser,)
    queryset = Project.objects.all()
    serializer_class = ShowQualityProjectSerializer

    def get_queryset(self):
        
        return self.queryset.filter(company__user=self.request.user,quality_checklist__question__typee=Question.Quality).distinct()


class ShowSafetyProjectView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser,)
    queryset = Project.objects.all()
    serializer_class = ShowSafetyProjectSerializer

    def get_queryset(self):
        return self.queryset.filter(company__user=self.request.user,safety_checklist__question__typee=Question.Safety).distinct()





class MaterialCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Material.objects.all()
    serializer_class = MaterialCreateSerializer
    def perform_create(self, serializer, **kwargs):
        
        try:
            company = Company.objects.get(user__email=self.request.user)
            maker = Vendor.objects.get(id=self.request.data.get('maker'))
        except Exception as e:
            raise serializers.ValidationError({'error':e})
        serializer.save(company=company, maker=maker)


class MaterialListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Material.objects.all()
    serializer_class = MaterialRUDSerializer
    def get_queryset(self):
        if self.request.user.user_type == User.TENENT:
            return self.queryset.filter(company__user=self.request.user)


class RUDMaterialView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Material.objects.all()
    serializer_class = MaterialRUDSerializer
    


class VendorLCView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    def get_queryset(self):
        
        return self.queryset.filter(company__user=self.request.user)
    
    def perform_create(self, serializer):
        company = Company.objects.get(user__email=self.request.user)
        serializer.save(company=company)


class RUDVendorlView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTenentUser)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer



class FaqLCView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer


class RUDFaqView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer

class BannerLCView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,IsTenentOrSuperUser)
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

import os
class RUDBannerView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,IsTenentOrSuperUser)
    queryset = Banner.objects.all()
    serializer_class = BannerRUDSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # print(instance)
        location = '%s/banner'%(settings.MEDIA_ROOT)
        multi_images  = json.loads(instance.multi_images)
        if len(multi_images) > 0:
            for pic in multi_images:
                # print(pic)
                filename = pic.strip("media/banner/")
                path = os.remove("%s/%s"%(location,filename))
                print(path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



class ReportListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,IsTenentUser)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            path = '%s/report/'%(settings.MEDIA_ROOT)
            filename = instance.download.strip(path)
            os.remove("%s/%s"%(path,filename))
        except Exception as e:
            pass
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


