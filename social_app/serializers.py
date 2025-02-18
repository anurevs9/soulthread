# social_app/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Forum, ForumPost, Media
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'profile']

    def get_full_name(self, obj):
        return obj.get_full_name()


class ProfileSerializer(serializers.Serializer):
    profile_pic = serializers.URLField(source='profile_pic.url', read_only=True)
    bio = serializers.CharField()

    class Meta:
        fields = ['profile_pic', 'bio']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    image = serializers.URLField(source='image.url', read_only=True, allow_null=True)
    file = serializers.URLField(source='file.url', read_only=True, allow_null=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'file', 'location', 'visibility', 'created_at', 'likes_count', 'comments_count']
        read_only_fields = ['created_at', 'likes_count', 'comments_count', 'user']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'post']


class ForumSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Forum
        fields = ['id', 'title', 'description', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_at', 'created_by']


class ForumPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    forum = ForumSerializer(read_only=True)

    class Meta:
        model = ForumPost
        fields = ['id', 'forum', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'forum']


class MediaSerializer(serializers.ModelSerializer):
    file = serializers.URLField(source='file.url', read_only=True)

    class Meta:
        model = Media
        fields = ['id', 'file', 'title', 'user', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

class FollowUnfollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with this ID does not exist.")
        return value