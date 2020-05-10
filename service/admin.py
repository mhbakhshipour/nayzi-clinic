from django.contrib import admin

from service.models import Service, ServiceGallery


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug', 'jalali_created_at')
    search_fields = ['title']


class ServiceGalleryAdmin(admin.ModelAdmin):
    list_display = ('description', 'jalali_created_at')
    search_fields = ['description']


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceGallery, ServiceGalleryAdmin)
