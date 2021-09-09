from accounts.models import *
import json
from django.contrib.auth import get_user_model

User = get_user_model()
def payment_create(payment):
    payment.status = Payment.PAYMENT_DONE
    payment.updated_at = timezone.now()
    payment.save()
    pass

def company_create(user, company, plan):

    user = User.objects.create_user(**user)
    user.user_type = User.TENENT
    user.save()
    contact_person = company.pop("contact_person")
    contact_person = User.objects.get(id = contact_person)
    company = Company.objects.create(user= user, contact_person=contact_person, **company)
    company.license_purchased = plan["license_count"]
    company.save()
    pass
# def company_create(company, plan):
#     pass