from django.db import models
from django.db.models import Manager
from django.utils.translation import ugettext as _
from jalali_date import datetime2jalali

from nayzi import settings


class FaqCategory(models.Model):
    title = models.CharField(_('title'), max_length=255, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    class Meta:
        db_table = 'faq_categories'
        verbose_name = _('faq_category')
        verbose_name_plural = _('faq_categories')

    def __str__(self):
        return self.title


class FaqManager(Manager):
    def get_faq_with_by_category(self, cat_id):
        return self.filter(cats__id=cat_id)


class Faq(models.Model):
    title = models.CharField(_('title'), max_length=255, unique=True)
    content = models.TextField(_('content'), null=False, blank=False)
    cats = models.ManyToManyField(verbose_name=_('categories'), to="FaqCategory", related_name='faq_cat', blank=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    objects = FaqManager()

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    class Meta:
        db_table = 'faqs'
        verbose_name = _('faq')
        verbose_name_plural = _('faqs')

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    contact_us_status_choices = (
        ('read', _('read')),
        ('unread', _('unread'))
    )

    full_name = models.CharField(_('full_name'), null=False, blank=False, max_length=500)
    email = models.EmailField(_('email'), null=False, blank=False, max_length=255)
    phone = models.CharField(_('phone'), null=False, blank=False, max_length=13)
    description = models.TextField(_('description'), null=False, blank=False, max_length=1024)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    status = models.CharField(_('status'), max_length=255, choices=contact_us_status_choices, default='unread')

    @property
    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'contact_us'
        verbose_name = _('contact_us')
        verbose_name_plural = _('contact_us')


class PromotionManager(Manager):
    def get_active_promotion(self):
        return self.filter(is_active=True)


class Promotion(models.Model):
    title = models.CharField(_('title'), max_length=255, unique=True)
    thumbnail = models.ImageField(_('thumbnail'), upload_to=settings.UPLOAD_DIRECTORIES['promotion_thumbnail'], blank=False, null=False)
    slug = models.CharField(max_length=255, verbose_name=_('slug'), unique=True, blank=False, null=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    is_active = models.BooleanField(_('is_active'), default=False)

    objects = PromotionManager()

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    class Meta:
        db_table = 'promotions'
        verbose_name = _('promotion')
        verbose_name_plural = _('promotions')

    def __str__(self):
        return self.title
