from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Manager
from django.utils.translation import ugettext as _
from froala_editor.fields import FroalaField
from jalali_date import datetime2jalali

from nayzi import settings


class BlogCategory(models.Model):
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
        db_table = 'blog_categories'
        verbose_name = _('blog_category')
        verbose_name_plural = _('blog_categories')

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_status_choices = (
        ('pending', _('pending')),
        ('accepted', _('accepted'))
    )

    comment = models.TextField(_('comment'), null=False, blank=False, max_length=500)
    email = models.EmailField(_('email'), null=False, blank=False, max_length=255)
    phone = models.CharField(_('phone'), null=False, blank=False, max_length=13)
    first_name = models.CharField(_('first_name'), null=False, blank=False, max_length=255)
    last_name = models.CharField(_('last_name'), null=False, blank=False, max_length=255)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    parent = models.ForeignKey(to='self', blank=True, null=True, on_delete=models.CASCADE, related_name='children',
                               verbose_name=_('parent'))
    status = models.CharField(_('status'), max_length=255, choices=comment_status_choices, default='pending')

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'comments'
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class CommentedItems(models.Model):
    comment = models.ForeignKey(to='Comment', on_delete=models.CASCADE, verbose_name=_('comment'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('content_type'))
    object_id = models.PositiveIntegerField(verbose_name=_('object_id'))
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def comment_first_name(self):
        return self.comment.first_name

    @property
    def comment_last_name(self):
        return self.comment.last_name

    @property
    def comment_title(self):
        return self.comment.comment

    @property
    def comment_email(self):
        return self.comment.email

    @property
    def comment_phone(self):
        return self.comment.phone

    @property
    def comment_status(self):
        return self.comment.status

    @property
    def comment_created_at(self):
        return datetime2jalali(self.comment.created_at).strftime('%y/%m/%d')

    @property
    def comment_parent(self):
        if self.comment.parent is None:
            return self.comment.parent
        return self.comment.parent.id

    def __str__(self):
        return self.comment.comment

    class Meta:
        db_table = 'commented_items'
        verbose_name = _('commented_items')
        verbose_name_plural = _('commented_items')


class BlogManager(Manager):
    def get_blog_with_by_category(self, cat_id):
        return self.filter(cats__id=cat_id)


class Blog(models.Model):
    title = models.CharField(_('title'), max_length=255, unique=True)
    description = models.TextField(_('description'), null=False, blank=False)
    seo_title = models.CharField(_('seo_title'), max_length=255, unique=True, blank=True, null=True)
    seo_description = models.TextField(_('seo_description'), null=True, blank=True)
    content = FroalaField()
    cats = models.ManyToManyField(verbose_name=_('categories'), to="BlogCategory", related_name='blog_cat', blank=True)
    time = models.IntegerField(_('time'), null=False, blank=False)
    comments = GenericRelation(CommentedItems, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    thumbnail = models.ImageField(_('thumbnail'), upload_to=settings.UPLOAD_DIRECTORIES['blog_thumbnail'])
    slug = models.CharField(max_length=255, verbose_name=_('slug'), unique=True)

    objects = BlogManager()

    def jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%y/%m/%d')

    class Meta:
        db_table = 'blog'
        verbose_name = _('blog')
        verbose_name_plural = _('blog')

    def __str__(self):
        return self.title
