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


admin.site.register(Faq, FaqAdmin)
admin.site.register(FaqCategory, FaqCategoryAdmin)
