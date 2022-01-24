from django.contrib import admin
from .models import User


class UserRef(admin.ModelAdmin):
    list_display = ['first_name','email','mobile','last_login']
admin.site.register(User,UserRef)
