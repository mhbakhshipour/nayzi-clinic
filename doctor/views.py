from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from nayzi.custom_view_mixins import ExpressiveListModelMixin
from doctor.models import *
from doctor.serializers import *


class ResultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class DoctorListView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = DoctorListSerializer
    plural_name = 'doctors_list'
    pagination_class = ResultPagination

    def get_queryset(self):
        queryset = Doctor.objects.all().order_by('order')
        return queryset


class DoctorCategoryListView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = DoctorCategoryListSerializer
    plural_name = 'doctor_categories_list'

    def get_queryset(self):
        queryset = DoctorCategory.objects.all().order_by('-created_at')
        return queryset


class DoctorListByCategoryView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = DoctorListSerializer
    plural_name = 'doctors_list_by_category'

    def get_queryset(self):
        cat_slug = self.kwargs['cat_slug']
        queryset = Doctor.objects.get_doctor_with_by_category(cat_slug).order_by('order')
        return queryset


class DoctorDetailView(ExpressiveListModelMixin, generics.ListAPIView):
    serializer_class = DoctorDetailSerializer
    plural_name = 'doctor'

    def get_queryset(self):
        slug = self.kwargs['slug']
        queryset = Doctor.objects.filter(slug=slug)
        return queryset
