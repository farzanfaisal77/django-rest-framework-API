from rest_framework import serializers
from .models import Post

from django.contrib.auth import get_user_model #makes sure we use correct model whether default or custom

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=("id", "author", "title", "body", "created_at",)
        read_only_fields=("author",)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=("id", "username",)