from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from posts.models import Post
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    read:
    Return the given post.

    list:
    Return a paginated list of all the existing posts.

    create:
    Create a new post instance.

    update:
    Update contents of the post. Will set views counter back to zero.

    partial_update:
    Update contents of the post. Will set views counter back to zero
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    http_method_names = ["get", "post", "patch", "put"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(views=0)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    read:
    Return the given user.

    list:
    Return a list of all the existing users.

    create:
    Create a new user instance.

    delete:
    Delete given user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    http_method_names = ["get", "post", "delete"]
