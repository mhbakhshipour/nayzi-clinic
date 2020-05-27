from rest_framework import serializers

from core.models import *


class FaqCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqCategory
        fields = ['id', 'title', 'jalali_created_at']


class FaqListSerializer(serializers.ModelSerializer):
    cats = FaqCategoryListSerializer(many=True)

    class Meta:
        model = Faq
        fields = ['id', 'title', 'content', 'jalali_created_at', 'cats']


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'full_name', 'email', 'phone', 'description', 'jalali_created_at', 'status']
