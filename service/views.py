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
        queryset = Service.objects.all().order_by('-created_at')
        return queryset


class ServiceDetailView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = ServiceDetailSerializer
    plural_name = 'service_detail'

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Service.objects.filter(pk=pk)
        return queryset
