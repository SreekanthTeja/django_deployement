from accounts.models import *
from buildcorn.models import License
from django.shortcuts import render
import json
from django.contrib.auth import get_user_model
from django.db.models import Q
import datetime
from rest_framework import serializers
from rest_framework.response import Response
from datetime import date
from dateutil.relativedelta import relativedelta
User = get_user_model()

today = date.today()


def licensee_create(company, plan):
    # created_at = datetime.date.today()
    # years = 1
    # result = created_at + datetime.timedelta(366 * years)
    # if years > 0:
    #     while result.year - created_at.year > years or created_at.month < result.month or created_at.day < result.day:
    #         result += datetime.timedelta(-1)
    

    # end_at = datetime.datetime.strftime(result, "%Y-%m-%d")
    # licens = License.objects.create(user=user, created_at=created_at,end_at=end_at )
    # licens.save()
    if plan["name"] == 'Annual Plan':
        annual = today +  relativedelta(months=12)
        end_at = datetime.datetime.strftime(annual, "%Y-%m-%d")
        licens = License.objects.create(company=company, created_at=today, end_at=end_at, tenure=12)
        licens.save()
    elif plan["name"] == 'Quaterly Plan':
        quaterly = today +  relativedelta(months=3)
        end_at = datetime.datetime.strftime(quaterly, "%Y-%m-%d")
        licens = License.objects.create(company=company, created_at=today, end_at=end_at, tenure=3)
        licens.save()
    else:
        month = today +  relativedelta(months=1)
        end_at = datetime.datetime.strftime(month, "%Y-%m-%d")
        licens = License.objects.create(company=company, created_at=today, end_at=end_at, tenure=1)
        licens.save()

def company_create(payment,user, company, plan):
    # print(plan)
    payment.status = Payment.PAYMENT_DONE
    payment.payment_mode = 'IBNK'
    payment.updated_at = timezone.now()
    print(user["email"],user["phone_number"])
    if User.objects.filter(Q(email__iexact=user["email"]) | Q(phone_number__iexact=user["phone_number"])).exists():
        return True
    
    if Company.objects.filter(gstin=company["gstin"]).exists():
        return True
    user = User.objects.create_user(**user)
    user.user_type = User.TENENT
    user.save()
    payment.user = user
    payment.save()
    company = Company.objects.create(user= user, **company)
    company.license_purchased = plan["license_count"]
    company.save()
    licensee_create(company, plan)