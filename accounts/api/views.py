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

User = get_user_model()
class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.user_type==User.SUPER_ADMIN


    
        
# class CompanyRDView(generics.RetrieveDestroyAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer

# class EmployeeSignup(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     def create(self, request, **kwargs):
#         cid = kwargs["cid"]
#         user = User.objects.create_user(**request.data)
#         company = Company.objects.filter(company_id= cid)
#         print(company)
#         company[0].employees.add(user.id)
#         return Response({"status":"Successfull registerd"})
# class EmployeeListAPIView(generics.RetrieveAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanyEmployeeListSerializer
#     lookup_field = "company_id"
    
# class ContactPersonAPIView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = ContactPersonSerializer

#     def get_queryset(self):
#         user = self.queryset.filter(user_type=User.SUPER_ADMIN)
#         return user


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

class OTPSendAPIView(views.APIView):
   def get(self,request,phoneno=None,format=None):
        otp = random.randint(100000, 999999)
        # Store Phone Number
        #phone = "7903102839";request.POST.get
        phone = str(phoneno)
        # Contstruc Message String
        message = str(otp) + ' is the verification code to access your Buildcron account. This verification code is valid for 5 mins. Please do not share it with anyone. Thanks, Squarow consultants pvt. ltd.'
        # Encode message
        message = urllib.parse.quote(message, safe='')
        # Construct API URL to send SMS
        url = "https://smsapi.24x7sms.com/api_2.0/SendSMS.aspx?APIKEY=WxSMoQhUSAZ&MobileNo=" + phone + "&SenderID=SQUROW&Message=" + message + "&ServiceName=TEMPLATE_BASED"
        # Run API
        r = requests.get(url)
        # Display API response
        print(r.text)
        print("SMS SENT...")
        return Response({'success':'Your OTP sent..'}, status=status.HTTP_200_OK)