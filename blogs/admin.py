from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import User, Addres, Agent,Lead

# Register your models here.

# class UserAdmin(BaseUserAdmin):
#     list_display = ('first_name','last_name','email','phone', 'username','last_login',)
    # list_filter = ('is_superuser',"phone")

admin.site.register(User)
admin.site.register(Addres)
admin.site.register(Agent)
admin.site.register(Lead)