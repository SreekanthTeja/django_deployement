from rest_framework import generics
from django.shortcuts import render
from rest_framework import views
from .serializers import *
from accounts.models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework import serializers
import random
from accounts.tasks import  send_otp
from accounts.api.utils import *
from buildcorn.models import Employee
from bigspace.permissions import *
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

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
    def delete(self, request, pk):
        user = User.objects.get(id=pk).delete()
        return Response({'status':'Deleted'})
   
    

class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    

class PlanReadView(generics.RetrieveAPIView):
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
            # return Response({
            #     "invoice_id": invoice_id,
            #     "status": Payment.PAYMENT_FAILED,
            #     "detail": "Payment failed",
            # })
            context = {
                "invoice_id": invoice_id,
                "status": "Payment failed",
                'time':payment.updated_at
            }
            # return Response(context)
            return render(request, 'accounts/payment_fail.html',context)
        # payment_create(payment)
        holder_data = payment.holder
        data = json.loads(holder_data)
        comp = company_create(payment,data["user_details"],data["company_details"], data["plan_details"])
        if comp:
            return render(request, "accounts/payment_user.html",{"status":"given email,phone number, gstin one of its already in use "})
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
        # context = {
        #     "invoice_id": invoice_id,
        #     "status": Payment.PAYMENT_DONE,
        #     "detail": "Payment success",
        # }
        context = {
            "invoice_id": invoice_id,
            "status": "Payment success",
            'by':data["user_details"]["first_name"],
            'time':payment.updated_at
        }
        # return Response(context)
        return render(request, 'accounts/payment_success.html',context)

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
            # "prefill":{
            #     "name": user_details["first_name"],
            #     "email":user_details["email"],
            #     "contact":user_details["phone_number"],
            # },
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







class OTPRequestAPIView(views.APIView):
    def post(self,request, **kwargs ):
        otp = random.randint(99999, 999999)
        # send_request = send_otp(request.data["phone_number"],str(otp))
        phone_number = request.data.get("phone_number",None)
        user_object = User.objects.filter(phone_number__iexact=phone_number, is_active=True).exists()
        if user_object:
            send_request = send_otp(phone_number,str(otp))
            print(send_request)
            if send_request['status']=='SENT':
                user = User.objects.get(phone_number=phone_number)
                try:
                    emp = Employee.objects.get(user=user)
                except Exception as e:
                    raise serializers.ValidationError("Sorry user is  not a employee")
                otp_obj, created = OTP.objects.get_or_create(otp=otp,user=user)
                if created:
                    otp_obj.save()
            return Response({"otp":otp,'Alert':"expires in a hour",'company':emp.company.name,'user_type':user.user_type})
        return Response({'error':'Your credentials not found'})

from rest_framework_simplejwt.tokens import RefreshToken
class OTPVerifyAPIView(TokenObtainPairView):
    def post(self, request):
        if OTP.objects.filter(otp=request.data["otp"],validated=False ).exists():
            otp = OTP.objects.get(otp=request.data["otp"]).delete()
            user = User.objects.get(phone_number=request.data["phone_number"])
            refresh = RefreshToken.for_user(user)
            return Response({ 
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username':user.first_name,
                'role':user.user_type
            })
        raise serializers.ValidationError({'status':"incorrect otp"})


