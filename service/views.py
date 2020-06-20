from django.shortcuts import render
from rest_framework import generics

from blog.views import ResultPagination
from nayzi.custom_view_mixins import ExpressiveListModelMixin
from service.models import Service
from service.serializers import *


class ServiceListView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = ServiceListSerializer
    plural_name = 'service_list'
    pagination_class = ResultPagination

    def get_queryset(self):
        queryset = Service.objects.all().order_by('order')
        return queryset


class ServiceDetailView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = ServiceDetailSerializer
    plural_name = 'service_detail'

    def get_queryset(self):
        slug = self.kwargs['slug']
        queryset = Service.objects.filter(slug=slug)
        return queryset
