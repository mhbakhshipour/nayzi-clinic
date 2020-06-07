from rest_framework import serializers

from service.models import Service, ServiceGallery


class ServiceGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceGallery
        fields = ['image', 'description']


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'thumbnail', 'slug']


class ServiceDetailSerializer(serializers.ModelSerializer):
    images = ServiceGallerySerializer(many=True)

    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'thumbnail', 'slug', 'images', 'seo_title', 'seo_description']
