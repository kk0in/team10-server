from rest_framework import serializers
from .models import *
from authentication.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'student_id', 'is_professor']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_by', 'created_at']


class CommentSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = ['content', 'created_by', 'created_at']


class PostCreateSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['title', 'created_by', 'created_at', 'content']


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'created_by', 'created_at', 'content', 'comment']


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'created_by', 'created_at', 'content']

    def create(self, validated_data):
        post = Post.objects.create(title=validated_data['title'], created_by=validated_data['created_by'], created_at=validated_data['created_at'], is_announcement=True)
        post.save()

        return post
