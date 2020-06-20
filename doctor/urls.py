from django.urls import path

from doctor.views import *

urlpatterns = [
    path('api/v1/doctor/list', DoctorListView.as_view(), name='api_get_doctor_list'),
    path('api/v1/doctor-category/list', DoctorCategoryListView.as_view(), name='api_get_doctor_category_list'),
    path('api/v1/doctor-by-category/list/<str:cat_slug>', DoctorListByCategoryView.as_view(), name='api_get_doctor_list_by_category'),
    path('api/v1/doctor/<str:slug>', DoctorDetailView.as_view(), name='api_get_doctor_detail')
]
