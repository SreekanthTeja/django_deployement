from accounts.models import *
from buildcorn.models import License
import json
from django.contrib.auth import get_user_model
import datetime
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
    print(plan)
    payment.status = Payment.PAYMENT_DONE
    payment.payment_mode = 'IBNK'
    payment.updated_at = timezone.now()
    # payment.save()
    user = User.objects.create_user(**user)
    user.user_type = User.TENENT
    user.save()
    payment.user = user
    payment.save()
    contact_person = company.pop("contact_person")
    contact_person = User.objects.get(id = contact_person)
    company = Company.objects.create(user= user, contact_person=contact_person, **company)
    company.license_purchased = plan["license_count"]
    company.save()
    licensee_create(user)