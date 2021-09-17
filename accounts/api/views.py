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
from rest_framework import views
import json
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.utils import *
from buildcorn.models import Employee

User = get_user_model()
class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.user_type==User.SUPER_ADMIN

class IsTenentOrUser(IsAdminUser):
    def has_permission(self, request, view):
        print("......",request.user)
        return  request.user.user_type=='TN'

"""
    SuperUsers list
"""
class SuperAdminListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(user_type=User.SUPER_ADMIN)



class CompanyCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,IsSuperUser,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyListView(generics.ListAPIView):
    permission_classes = ( IsAuthenticated,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
class CompanyRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Company.objects.all()
    serializer_class = CompanyUpdateSerializer
    def update(self, request, *args, **kwargs):
        data = request.data
        # print(data["user"]["id"])
        if not data["user"].get("id"):
            print(True)
            raise serializers.ValidationError({'error':'user object id  required'})
        user_instance = User.objects.get(id= data["user"].get("id"))
        print(user_instance)
        if "email" in data["user"]:
            user_instance.email = data["user"].get("email")
        if "first_name" in data["user"]:
            user_instance.first_name = data["user"].get("first_name")
        if "phone_number" in data["user"]:
            user_instance.first_name = data["user"].get("phone_number")
        user_instance.save()
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
                company_instance.city= data["city"]
            if "pincode" in data :
                company_instance.pincode= data["pincode"]
            if "addres" in data :
                company_instance.addres= data["addres"]
            if "license_purchased" in data :
                company_instance.license_purchased= data["license_purchased"]
            company_instance.save()
            return Response({'status':"Updated"})
        except Exception as e:
            pass
    def delete(self, request, pk):
        user = User.objects.get(id=pk).delete()
        return Response({'status':'Deleted'})

class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    
    
"""Company apis end"""

class PaymentResponseView(views.APIView):
    def get(self, request, *args, **kwargs):
        invoice_id = request.GET.get("razorpay_invoice_id")
        response = fetch_payment_link(invoice_id=invoice_id)
        payment = Payment.objects.get(payment_id=invoice_id)
        status = response["status"]
        # print(response)
        if status != "paid":
            payment.status = Payment.PAYMENT_FAILED
            payment.save()
            return Response({
                "invoice_id": invoice_id,
                "status": Payment.PAYMENT_FAILED,
                "detail": "Payment failed",
            })
        # payment_create(payment)
        holder_data = payment.holder
        data = json.loads(holder_data)
        comp = company_create(payment,data["user_details"],data["company_details"], data["plan_details"])
        # print(comp) 
        # if comp["status"] == "exists":
        #     return Response({'status':"Sorry the given  Email or Phone number already used"})
        # msg_html = render_to_string('user_invoice_mail.html', {'payment': payment})
        # send_mail(
        #     'Payment Success',
        #     "Your Subscription activation success",
        #     'support@buildcron.com',
        #     [request.user.email],
        #     html_message=msg_html,
        # )
        context = {
            "invoice_id": invoice_id,
            "status": Payment.PAYMENT_DONE,
            "detail": "Payment success",
        }
        return Response(context)

from accounts.razorpayment import *
class PaymentView(views.APIView):
    def post(self, request, *args, **kwargs):
        indata = request.data
        user_details = indata.get("user_details",None)
        company_details = indata.get("company_details", None)
        plan_details = indata.get("plan_details", None)
        
        if user_details == None or company_details==None or plan_details==None:
            raise serializers.ValidationError("some details are missing")
        amount = float(plan_details["ammount"])
        # cgst = float(indata('cgst'))
        # sgst = float(indata('sgst'))
        # gst = cgst+sgst
        # gst_amount = amount+(amount/100)*plan_details["gst"]
        # final_amount = round(amount, 2)
        # print(user_details["first_name"])
        schema = request.scheme
        absolute_url = request.META['HTTP_HOST']
        print(schema, type(schema))
        url = "{schema}://{absolute_url}/accounts/api/payment/success".format(schema = schema, absolute_url =absolute_url)
        data = {
            # "customer": user_details["first_name"],
            "type": "link",
            "amount": amount*100,
            "currency": "INR",
            "description": f"Complete payment for {amount} INR",
            "callback_url": url,
            "callback_method": "get"
        }
        response = create_payment_link(data)
        payment = Payment()

        payment.payment_id = response["id"]
        payment.holder=json.dumps(indata)
        payment.status = Payment.PAYMENT_PENDING
        payment.company_name = company_details["name"]
        payment.amount = amount
        payment.save()
        # print(response)
        return Response({
            "next": response["short_url"],
            'status': payment.status,
            'payment_id': payment.payment_id
        })

class RestPasswordAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()
    lookup_field = 'email'
    def update(self, request,*args, **kwargs):
        instance = self.get_object()
        if not User.objects.filter(email=request.user).exists():
            raise serializers.ValidationError({"error":"We couldnt find this email in our database"})
        password = request.data.get('old_password',None)
        if password and not instance.check_password(password):
            raise serializers.ValidationError({'status':'Old password is wrong'})

        if len(request.data["new_password"]) < 8:
            raise serializers.ValidationError({"error":"Password must be min 8 characters"})
        if request.data["new_password"] != request.data["confirm_new_password"]:
            raise serializers.ValidationError({"error":"Two password didn't match"})
        password = request.data.get('confirm_new_password') 

        instance.set_password(password)
        instance.save()
        return Response({"status":'Password reset done successfully'})


class ForgotPasswordAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer
    lookup_field = 'email'
    def update(self, request,*args, **kwargs):
        instance = self.get_object()
        print(instance)
        # if not User.objects.filter(email=request.user).exists():
        #     raise serializers.ValidationError({"error":"We couldnt find this email in our database"})
        # password = request.data.get('old_password',None)
        # if password and not instance.check_password(password):
        #     raise serializers.ValidationError({'status':'Old password is wrong'})

        # if len(request.data["new_password"]) < 8:
        #     raise serializers.ValidationError({"error":"Password must be min 8 characters"})
        # if request.data["new_password"] != request.data["confirm_new_password"]:
        #     raise serializers.ValidationError({"error":"Two password didn't match"})
        # password = request.data.get('confirm_new_password') 

        # instance.set_password(password)
        # instance.save()
        # return Response({"status":'Password reset done successfully'})


class UserUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,IsTenentOrUser)
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

from django.utils import timezone
from datetime import timedelta, datetime
# dt = datetime.today().replace(microsecond=0)
class Test(views.APIView):
    def get(self, request):
        current_time = timezone.now() + timedelta(hours=1)
        print(current_time)
        return Response("ok")


