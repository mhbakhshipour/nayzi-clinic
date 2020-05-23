from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from doctor.models import *


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job_position', 'mobile', 'categories', 'slug', 'jalali_join_at', 'jalali_created_at')
    search_fields = ['full_name', 'job_position', 'mobile']

    def categories(self, obj):
        if obj.cats.all() is not None:
            a = []
            for c in obj.cats.all():
                a.append(str(c.title))
            return a


class DoctorCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'jalali_created_at')
    search_fields = ['title']


class DoctorCertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'jalali_created_at')
    search_fields = ['title']


class DoctorEducationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('uni', 'jalali_start_date', 'jalali_end_date',  'jalali_created_at')
    search_fields = ['uni']


admin.site.register(DoctorCategory, DoctorCategoryAdmin)
admin.site.register(DoctorCertificate, DoctorCertificateAdmin)
admin.site.register(DoctorEducation, DoctorEducationAdmin)
admin.site.register(Doctor, DoctorAdmin)
