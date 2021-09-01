from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ('email','phone','user_id','user_type',)
    # list_filter = ('is_admin',)
    


admin.site.register(User)
# admin.site.register(User)
admin.site.register(Company)
admin.site.register(Addres)