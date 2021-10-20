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

def license_serial_generation(license_last_id,license_purchased_count):
    end = license_last_id + license_purchased_count
    license_ids = [ {"id":f"{i:03}","active":True} for i in range(license_last_id+1,end+1)]
    return {
        "license_ids": license_ids,
        "last_id": int(license_ids[-1]["id"])
    }

# license_serial_generation()

# def licensee_create(company, plan):
#     try:
#         if plan["name"] == 'Annual Plan':
#             annual = today +  relativedelta(months=12)
#             end_at = datetime.datetime.strftime(annual, "%Y-%m-%d")
#             licens = License.objects.create(company=company, created_at=today, end_at=end_at, tenure=12)
#             licens.save()
#         elif plan["name"] == 'Quaterly Plan':
#             quaterly = today +  relativedelta(months=3)
#             end_at = datetime.datetime.strftime(quaterly, "%Y-%m-%d")
#             licens = License.objects.create(company=company, created_at=today, end_at=end_at, tenure=3)
#             licens.save()
#         else:
#             month = today +  relativedelta(months=1)
#             end_at = datetime.datetime.strftime(month, "%Y-%m-%d")
#             licens = License.objects.create(company=company, created_at=today, end_at=end_at, tenure=1)
#             licens.save()
#     except Exception as e:
#         raise serializers.ValidationError({'error':e})

def licensee_create(company, plan):
    try:
        last_obj = 0 if not License.objects.first() else License.objects.first().last_license_id
        license_purchased_count = plan["license_count"]
        if plan["name"] == 'Annual Plan':
            annual = today +  relativedelta(months=12)
            end_at = datetime.datetime.strftime(annual, "%Y-%m-%d")
            licens, created = License.objects.get_or_create(company=company, created_at=today, end_at=end_at, tenure=12)
            if created:
                licens_sequence_ids = license_serial_generation(last_obj, license_purchased_count)
                licens.emp_license_ids = json.dumps(licens_sequence_ids["license_ids"])
                print(type(licens_sequence_ids["last_id"]))
                licens.last_license_id=licens_sequence_ids["last_id"]
                licens.save()
            licens.save()
        elif plan["name"] == 'Quaterly Plan':
            quaterly = today +  relativedelta(months=3)
            end_at = datetime.datetime.strftime(quaterly, "%Y-%m-%d")
            licens, created = License.objects.get_or_create(company=company, created_at=today, end_at=end_at, tenure=3)
            if created:
                licens_sequence_ids = license_serial_generation(last_obj, license_purchased_count)
                licens.emp_license_ids = json.dumps(licens_sequence_ids["license_ids"])
                print(type(licens_sequence_ids["last_id"]))
                licens.last_license_id=licens_sequence_ids["last_id"]
                licens.save()
        else:
            month = today +  relativedelta(months=1)
            end_at = datetime.datetime.strftime(month, "%Y-%m-%d")
            licens, created = License.objects.get_or_create(company=company, created_at=today, end_at=end_at, tenure=1)
            if created:
                licens_sequence_ids = license_serial_generation(last_obj, license_purchased_count)
                licens.emp_license_ids = json.dumps(licens_sequence_ids["license_ids"])
                print(type(licens_sequence_ids["last_id"]))
                licens.last_license_id=licens_sequence_ids["last_id"]
                licens.save()
            
    except Exception as e:
        raise serializers.ValidationError({'error':e})

def company_create(payment,user, company, plan):
    payment.status = Payment.PAYMENT_DONE
    payment.payment_mode = 'IBNK'
    payment.updated_at = timezone.now()
    print(user["email"],user["phone_number"])
    if User.objects.filter(Q(email__iexact=user["email"]) | Q(phone_number__iexact=user["phone_number"])).exists():
        return True
    
    if Company.objects.filter(gstin=company["gstin"]).exists():
        return True
    else:
        user = User.objects.create_user(**user)
        user.user_type = User.TENENT
        user.save()
        payment.user = user
        payment.save()
        company = Company.objects.create(user= user, **company)
        company.license_purchased = plan["license_count"]
        company.save()
        licensee_create(company, plan)