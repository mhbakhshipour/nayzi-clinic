from django.urls import path

from core.views import *

urlpatterns = [
    path('api/v1/faq/list', FaqListView.as_view(), name='api_get_faq_list'),
    path('api/v1/faq-category/list', FaqCategoryListView.as_view(), name='api_get_faq_category_list'),
    path('api/v1/faq-by-category/list/<int:cat_id>', FaqListByCategoryView.as_view(), name='api_get_faq_list_by_category'),
    path('api/v1/contact-us-form', ContactUsViewSet.as_view(), name='contact_us_form'),
]
