from django.urls import path

from blog.views import *

urlpatterns = [
    path('api/v1/blog/list', BlogListView.as_view(), name='api_get_blog_list'),
    path('api/v1/blog-category/list', BlogCategoryListView.as_view(), name='api_get_blog_category_list'),
    path('api/v1/blog-by-category/list/<int:cat_id>', BlogListByCategoryView.as_view(), name='api_get_blog_list_by_category'),
    path('api/v1/blog/<int:pk>', BlogDetailView.as_view(), name='api_get_blog_detail'),
    path('api/v1/comment/<str:content_type>/<int:object_id>', CommentView.as_view(), name='api_create_comment'),
]
