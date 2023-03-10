# Generated by Django 3.0.6 on 2020-08-15 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=500, verbose_name='full_name')),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
                ('phone', models.CharField(max_length=13, verbose_name='phone')),
                ('description', models.TextField(max_length=1024, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('status', models.CharField(choices=[('read', 'read'), ('unread', 'unread')], default='unread', max_length=255, verbose_name='status')),
            ],
            options={
                'verbose_name': 'contact_us',
                'verbose_name_plural': 'contact_us',
                'db_table': 'contact_us',
            },
        ),
        migrations.CreateModel(
            name='FaqCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('seo_title', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='seo_title')),
                ('seo_description', models.TextField(blank=True, null=True, verbose_name='seo_description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'faq_category',
                'verbose_name_plural': 'faq_categories',
                'db_table': 'faq_categories',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('thumbnail', models.ImageField(upload_to='promotion_thumbnail', verbose_name='thumbnail')),
                ('slug', models.CharField(max_length=255, unique=True, verbose_name='slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
            ],
            options={
                'verbose_name': 'promotion',
                'verbose_name_plural': 'promotions',
                'db_table': 'promotions',
            },
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('seo_title', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='seo_title')),
                ('seo_description', models.TextField(blank=True, null=True, verbose_name='seo_description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('cats', models.ManyToManyField(related_name='faq_cat', to='core.FaqCategory', verbose_name='categories')),
            ],
            options={
                'verbose_name': 'faq',
                'verbose_name_plural': 'faqs',
                'db_table': 'faqs',
            },
        ),
    ]
