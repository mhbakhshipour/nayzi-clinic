from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from nayzi.custom_view_mixins import ExpressiveListModelMixin
from blog.models import *
from blog.serializers import *


class ResultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class BlogListView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = BlogListSerializer
    plural_name = 'blog_list'
    pagination_class = ResultPagination

    def get_queryset(self):
        queryset = Blog.objects.all().order_by('-created_at')
        return queryset


class BlogCategoryListView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = BlogCategoryListSerializer
    plural_name = 'blog_category_list'

    def get_queryset(self):
        queryset = BlogCategory.objects.all().order_by('-created_at')
        return queryset


class BlogListByCategoryView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = BlogListSerializer
    plural_name = 'blog_list_by_category'

    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
        queryset = Blog.objects.get_blog_with_by_category(cat_id).order_by('-created_at')
        return queryset


class BlogDetailView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = BlogDetailSerializer
    plural_name = 'blog'

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Blog.objects.filter(pk=pk)
        return queryset


class CommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    singular_name = 'comment_created'

    def perform_create(self, serializer):
        content_type = ContentType.objects.get(model=self.kwargs.get('content_type'))
        serializer.save(content_type=content_type.id, object_id=self.kwargs.get('object_id'))
