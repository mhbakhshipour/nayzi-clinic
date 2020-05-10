from django.contrib import admin

from blog.models import *


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'time', 'slug', 'categories', 'jalali_created_at')
    search_fields = ['title']

    def categories(self, obj):
        if obj.cats.all() is not None:
            a = []
            for c in obj.cats.all():
                a.append(str(c.title))
            return a


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug', 'jalali_created_at')
    search_fields = ['title']


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comment', 'email', 'phone', 'first_name', 'last_name', 'parent', 'status', 'jalali_created_at')
    search_fields = ['comment']
    list_filter = ('status',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Comment, CommentsAdmin)
# admin.site.register(CommentedItems)
