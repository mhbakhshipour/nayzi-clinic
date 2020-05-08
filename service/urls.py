from django.urls import path

from service.views import *

urlpatterns = [
    path('api/v1/services/list', ServiceListView.as_view(), name='api_get_service_list'),
    path('api/v1/services/<int:pk>', ServiceDetailView.as_view(), name='api_get_service_detail'),
]
