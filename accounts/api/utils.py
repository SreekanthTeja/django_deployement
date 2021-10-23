from accounts.models import *
from buildcorn.models import License
import json
from django.contrib.auth import get_user_model
from django.db.models import Q
import datetime
from rest_framework import serializers
from rest_framework.response import Response
User = get_user_model()

def licensee_create(user):
    created_at = datetime.date.today()
    years = 1
    result = created_at + datetime.timedelta(366 * years)
    if years > 0:
        while result.year - created_at.year > years or created_at.month < result.month or created_at.day < result.day:
            result += datetime.timedelta(-1)
    

    end_at = datetime.datetime.strftime(result, "%Y-%m-%d")
    licens = License.objects.create(user=user, created_at=created_at,end_at=end_at )
    licens.save()



# def payment_create(payment):
#     pass

def company_create(payment,user, company, plan):
    # print(plan)
    payment.status = Payment.PAYMENT_DONE
    payment.payment_mode = 'IBNK'
    payment.updated_at = timezone.now()
    # payment.save()
    print(user["email"],user["phone_number"])
    if User.objects.filter(Q(email__iexact=user["email"]) | Q(phone_number__iexact=user["phone_number"])):
    
        raise serializers.ValidationError("Sorry given email or phone number already used ")
    user = User.objects.create_user(**user)
    user.user_type = User.TENENT
    user.save()
    payment.user = user
    payment.save()
    company = Company.objects.create(user= user, **company)
    company.license_purchased = plan["license_count"]
    company.save()
    licensee_create(user)