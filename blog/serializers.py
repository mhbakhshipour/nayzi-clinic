from rest_framework import serializers

from authentication.serializers import validate_email, validate_mobile_number
from blog.models import *


class BlogCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'title', 'description', 'thumbnail', 'slug']


class BlogListSerializer(serializers.ModelSerializer):
    cats = BlogCategoryListSerializer(many=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'thumbnail', 'slug', 'jalali_created_at', 'time', 'cats']


class CommentsSerializer(serializers.ModelSerializer):
    read_only_fields = ('comment_id',)

    class Meta:
        model = CommentedItems
        fields = ['comment_id', 'comment_title', 'comment_first_name', 'comment_last_name', 'comment_created_at',
                  'comment_parent', 'comment_status']


class BlogDetailSerializer(serializers.ModelSerializer):
    cats = BlogCategoryListSerializer(many=True)
    comments = CommentsSerializer(many=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'content', 'cats', 'time', 'comments', 'thumbnail', 'slug',
                  'jalali_created_at', 'seo_title', 'seo_description', 'created_at']


class CommentedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentedItems
        fields = ['comment', 'content_type', 'object_id']


class CommentSerializer(serializers.Serializer):
    comment = serializers.CharField(required=True)
    email = serializers.CharField(required=True, validators=[validate_email])
    phone = serializers.IntegerField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    parent = serializers.IntegerField(required=False)

    def create(self, validated_data):
        if validated_data.get('parent') is not None:
            comment = Comment(
                comment=validated_data['comment'],
                email=validated_data['email'],
                phone=validated_data['phone'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                parent_id=validated_data['parent']
            )
            comment.save()
            commented_item = CommentedItems(comment=comment, content_type_id=validated_data['content_type'],
                                            object_id=validated_data['object_id'])
            commented_item.save()
            return comment
        else:
            comment = Comment(
                comment=validated_data['comment'],
                email=validated_data['email'],
                phone=validated_data['phone'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
            comment.save()
            commented_item = CommentedItems(comment=comment, content_type_id=validated_data['content_type'],
                                            object_id=validated_data['object_id'])
            commented_item.save()
            return comment

    def to_representation(self, instance):
        return {'status': 'ok', 'massage': 'comment created'}
