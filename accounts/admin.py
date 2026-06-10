from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CUChangeForm, CUCreationForm

class CustomUserAdmin(UserAdmin):
    add_form= CUCreationForm
    form=CUChangeForm
    model=CustomUser
    list_display=["email", "username", "name", "is_staff",]
    fieldsets=UserAdmin.fieldsets + ((None, {"fields": ("name",)}),)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "name", "password1", "password2"),
        }),)
    
admin.site.register(CustomUser, CustomUserAdmin)