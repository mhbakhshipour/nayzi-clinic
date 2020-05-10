from django.contrib import admin

from authentication.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'first_name', 'last_name', 'email', 'national_code', 'jalali_birth_date', 'jalali_created_at', 'jalali_verified_at', 'is_staff')
    search_fields = ['mobile', 'email', 'first_name', 'last_name']
    list_filter = ('is_staff',)


admin.site.register(User, UserAdmin)
