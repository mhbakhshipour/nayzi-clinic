from django.db import models
from django.db.models import Manager
from django.utils.translation import ugettext as _
from froala_editor.fields import FroalaField
from jalali_date import datetime2jalali, date2jalali

from nayzi import settings


class DoctorEducation(models.Model):
    uni = models.CharField(_('uni'), max_length=255, null=False, blank=False)
    start_date = models.DateField(_('start_date'), blank=False, null=False)
    end_date = models.DateField(_('end_date'), blank=False, null=False)
    description = models.TextField(_('description'), null=False, blank=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    def jalali_start_date(self):
        return date2jalali(self.start_date).strftime('%y')

    def jalali_end_date(self):
        return date2jalali(self.end_date).strftime('%y')

    class Meta:
        db_table = 'doctor_educations'
        verbose_name = _('doctor_education')
        verbose_name_plural = _('doctor_educations')

    def __str__(self):
        return self.uni


class DoctorCertificate(models.Model):
    title = models.CharField(_('title'), max_length=255, null=False, blank=False)
    description = models.TextField(_('description'), null=False, blank=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    class Meta:
        db_table = 'doctor_certificates'
        verbose_name = _('doctor_certificate')
        verbose_name_plural = _('doctor_certificates')

    def __str__(self):
        return self.title


class DoctorCategory(models.Model):
    title = models.CharField(_('title'), max_length=255, null=False, blank=False, unique=True)
    description = models.TextField(_('description'), null=False, blank=False)
    seo_title = models.CharField(_('seo_title'), max_length=255, unique=True, blank=True, null=True)
    seo_description = models.TextField(_('seo_description'), null=True, blank=True)
    thumbnail = models.ImageField(_('thumbnail'), upload_to=settings.UPLOAD_DIRECTORIES['category_thumbnail'])
    slug = models.CharField(_('slug'), max_length=255, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    class Meta:
        db_table = 'doctor_categories'
        verbose_name = _('doctor_category')
        verbose_name_plural = _('doctor_categories')

    def __str__(self):
        return self.title


class DoctorManager(Manager):
    def get_doctor_with_by_category(self, cat_slug):
        return self.filter(cats__slug=cat_slug)


class Doctor(models.Model):
    full_name = models.CharField(_('full_name'), max_length=255, unique=True)
    job_position = models.CharField(_('job_position'), max_length=255)
    about = FroalaField()
    cats = models.ManyToManyField(verbose_name=_('categories'), to="DoctorCategory", related_name='doctor_cat', blank=True)
    educations = models.ManyToManyField(verbose_name=_('educations'), to="DoctorEducation", related_name='doctor_edu', blank=True)
    certificates = models.ManyToManyField(verbose_name=_('certificates'), to="DoctorCertificate", related_name='doctor_cer', blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    join_at = models.DateField(_('join_at'), blank=False, null=False)
    thumbnail = models.ImageField(_('thumbnail'), upload_to=settings.UPLOAD_DIRECTORIES['doctor_thumbnail'])
    slug = models.CharField(max_length=255, verbose_name=_('slug'), unique=True)
    mobile = models.CharField(_('mobile'), max_length=20, null=True, blank=True)
    twitter_link = models.URLField(_('twitter_link'), max_length=512, null=True, blank=True)
    linkedin_link = models.URLField(_('linkedin_link'), max_length=512, null=True, blank=True)
    instagram_link = models.URLField(_('instagram_link'), max_length=512, null=True, blank=True)
    seo_title = models.CharField(_('seo_title'), max_length=255, unique=True, blank=True, null=True)
    seo_description = models.TextField(_('seo_description'), null=True, blank=True)
    order = models.SmallIntegerField(_('order'), blank=False, null=False, unique=True)

    objects = DoctorManager()

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    def jalali_join_at(self):
        return date2jalali(self.join_at).strftime('%y/%m/%d')

    class Meta:
        db_table = 'doctors'
        verbose_name = _('doctor')
        verbose_name_plural = _('doctors')

    def __str__(self):
        return self.full_name
