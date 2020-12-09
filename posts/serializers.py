from django.contrib.auth.models import User
from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Post
        fields = ("id", "content", "views", "owner")
        read_only_fields = (
            "id",
            "views",
            "owner",
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, view_name="post-detail", read_only=True
    )
    password = serializers.CharField(write_only=True)

    # Crude user registration
    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = User
        fields = ("id", "username", "posts", "password")
        read_only_fields = (
            "id",
            "posts",
        )
