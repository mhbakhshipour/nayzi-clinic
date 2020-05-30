from django.db import models
from django.utils.translation import ugettext as _
from jalali_date import datetime2jalali

from nayzi import settings


class ServiceGallery(models.Model):
    image = models.ImageField(_('image'), upload_to=settings.UPLOAD_DIRECTORIES['service_gallery'])
    description = models.TextField(_('description'), blank=False, null=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    class Meta:
        db_table = 'service_galleries'
        verbose_name = _('service_gallery')
        verbose_name_plural = _('service_galleries')

    def __str__(self):
        return self.description


class Service(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(_('description'), blank=False, null=False)
    thumbnail = models.ImageField(_('thumbnail'), upload_to=settings.UPLOAD_DIRECTORIES['service_thumbnail'],
                                  blank=True, null=True)
    images = models.ManyToManyField(verbose_name=_('images'), to="ServiceGallery", related_name='service_gallery',
                                    blank=True)
    slug = models.CharField(_('slug'), max_length=255, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    class Meta:
        db_table = 'services'
        verbose_name = _('service')
        verbose_name_plural = _('services')

    def __str__(self):
        return self.title
