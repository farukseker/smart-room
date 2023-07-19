from django.contrib import admin
from Account.models import CustomUserModel
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUserModel)
class CustomAdmin(UserAdmin):
    model = CustomUserModel


