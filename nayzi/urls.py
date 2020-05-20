"""nayzi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from authentication.urls import urlpatterns as authentication_urls
from service.urls import urlpatterns as service_urls
from blog.urls import urlpatterns as blog_urls
from core.urls import urlpatterns as core_urls
from doctor.urls import urlpatterns as doctor_urls
from nayzi import settings

admin.site.site_header = "پنل مدیریت نای ذی"
admin.site.site_title = "پنل مدیریت نای ذی"
admin.site.index_title = "پنل مدیریت نای ذی"

imported_urls = [
    *authentication_urls,
    *service_urls,
    *blog_urls,
    *core_urls,
    *doctor_urls,
]

urlpatterns = [
                  path('admin/', admin.site.urls),
                  *imported_urls,
                  url(r'^api-auth/', include('rest_framework.urls'))
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL,
                                                                           document_root=settings.MEDIA_ROOT)
