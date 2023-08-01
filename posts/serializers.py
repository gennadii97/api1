from rest_framework import serializers

from .models import Posts, Like


class PostsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Posts
        fields = "__all__"


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


