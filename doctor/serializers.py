from rest_framework import serializers

from doctor.models import *


class DoctorCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCategory
        fields = ['id', 'title', 'description', 'thumbnail', 'slug', 'seo_title', 'seo_description']


class DoctorEducationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorEducation
        fields = ['id', 'uni', 'jalali_start_date', 'jalali_end_date', 'description', 'jalali_created_at']


class DoctorCertificateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCertificate
        fields = ['id', 'title', 'description', 'jalali_created_at']


class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'full_name', 'job_position', 'thumbnail', 'slug', 'mobile', 'twitter_link', 'linkedin_link',
                  'instagram_link']


class DoctorDetailSerializer(serializers.ModelSerializer):
    cats = DoctorCategoryListSerializer(many=True)
    educations = DoctorEducationListSerializer(many=True)
    certificates = DoctorCertificateListSerializer(many=True)

    class Meta:
        model = Doctor
        fields = ['id', 'full_name', 'job_position', 'about', 'cats', 'educations', 'certificates', 'mobile',
                  'thumbnail', 'slug', 'jalali_join_at', 'jalali_created_at', 'twitter_link', 'linkedin_link',
                  'instagram_link', 'seo_title', 'seo_description']
