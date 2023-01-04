from django.contrib import admin

from backend import models

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone_no',
        'country',
        'is_verified',
        'is_staff',
        'is_active',
        'created_at',
        'updated_at'
    )
    
admin.site.register(models.User, UserAdmin)