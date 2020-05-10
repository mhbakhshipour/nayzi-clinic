from django.db import models
from django.db.models import Manager
from django.utils.translation import ugettext as _
from jalali_date import datetime2jalali


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
