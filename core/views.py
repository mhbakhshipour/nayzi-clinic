from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics

from blog.models import Blog
from core.models import *
from core.serializers import *
from nayzi.custom_view_mixins import ExpressiveListModelMixin, ExpressiveCreateContactUsViewSetModelMixin
from service.models import Service


class FaqListView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = FaqListSerializer
    plural_name = 'faq_list'

    def get_queryset(self):
        queryset = Faq.objects.all().order_by('-created_at')
        return queryset


class FaqCategoryListView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = FaqCategoryListSerializer
    plural_name = 'faq_category_list'

    def get_queryset(self):
        queryset = FaqCategory.objects.all().order_by('-created_at')
        return queryset


class FaqListByCategoryView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = FaqListSerializer
    plural_name = 'faq_list_by_category'

    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
        queryset = Faq.objects.get_faq_with_by_category(cat_id).order_by('-created_at')
        return queryset


class ContactUsViewSet(ExpressiveCreateContactUsViewSetModelMixin, generics.CreateAPIView):
    serializer_class = ContactUsSerializer
    singular_name = 'contact_us_form_created'


class PromotionListViewSet(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = PromotionListSerializer
    plural_name = 'promotions_list'

    def get_queryset(self):
        queryset = Promotion.objects.get_active_promotion().order_by('-created_at')
        return queryset


class SearchViewSet(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = SearchSerializer
    plural_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('query')
        blog_lookup = (Q(title__icontains=query) | Q(description__icontains=query))
        service_lookup = (Q(title__icontains=query) | Q(description__icontains=query))

        blog = {'blog': list(
            Blog.objects.filter(blog_lookup).distinct().values('id', 'title', 'description', 'thumbnail', 'slug'))}

        service = {'services': list(
            Service.objects.filter(service_lookup).distinct().values('id', 'title', 'description', 'thumbnail', 'slug'))}

        queryset = [blog, service]
        return queryset
