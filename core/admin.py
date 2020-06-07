from django import forms
from django.contrib import admin

from core.models import *


class FaqAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'categories', 'jalali_created_at')
    search_fields = ['title']

    def categories(self, obj):
        if obj.cats.all() is not None:
            a = []
            for c in obj.cats.all():
                a.append(str(c.title))
            return a


class FaqCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'jalali_created_at')
    search_fields = ['title']


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'phone', 'description', 'status']
        labels = {
            'full_name': 'نام',
            'email': 'ایمیل',
            'phone': 'شماره تماس',
            'description': 'متن',
            'status': 'وضعیت',
        }


class ContactUsAdmin(admin.ModelAdmin):
    form = ContactUsForm
    list_display = ('full_name', 'email', 'phone', 'jalali_created_at', 'status')
    list_filter = ('status',)
    search_fields = ['description', 'full_name', 'email', 'phone']


class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'jalali_created_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ['title', 'slug']


admin.site.register(Faq, FaqAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(FaqCategory, FaqCategoryAdmin)
admin.site.register(Promotion, PromotionAdmin)
