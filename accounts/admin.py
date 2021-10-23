from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from django.contrib.auth import get_user_model
User = get_user_model()
# class UserAdmin(BaseUserAdmin):
#     list_display = ('email','phone_number',"user_type")
    # list_filter = ('is_admin',)
# admin.site.register(User, UserAdmin )
admin.site.register(Plan)
admin.site.register(User)
admin.site.register(Company)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id','status',"amount")

admin.site.register(Payment, PaymentAdmin)