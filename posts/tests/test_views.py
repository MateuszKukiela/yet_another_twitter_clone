import json

import factory.fuzzy
from rest_framework import status
from rest_framework.test import APITestCase

from posts.factories import PostFactory, UserFactory
from posts.models import Post
from posts.serializers import PostSerializer


class TestApi(APITestCase):
    def test_get_posts(self):
        # Test getting all posts
        posts = PostFactory.create_batch(4)
        response = self.client.get("/posts/", format="json")
        post_content = json.dumps(PostSerializer(posts, many=True).data)
        response_content = json.dumps(response.json()["results"])
        self.assertJSONEqual(response_content, post_content)

    def test_post_posts(self):
        # Without account
        response = self.client.post("/posts/", {"content": "test_content"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # With account
        number_of_posts_before = Post.objects.count()
        user = UserFactory()
        self.client.force_authenticate(user)
        response = self.client.post("/posts/", {"content": "test_content"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert Post.objects.count() == number_of_posts_before + 1

        # Too long message
        content = factory.fuzzy.FuzzyText(length=200).fuzz()
        response = self.client.post("/posts/", {"content": content})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_counter(self):
        # Test counter of post views
        post = PostFactory()
        assert post.views == 0
        for i in range(10):
            self.client.get(f"/posts/{post.id}/", format="json")
        post = Post.objects.get(id=post.id)
        assert post.views == 10

    def test_view_counter_edit(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        # Sally creates a post
        response = self.client.post("/posts/", {"content": "test_content"})
        post_id = json.dumps(response.json()["id"])
        post = Post.objects.get(id=post_id)

        # and it has 0 views
        assert post.views == 0

        # After a while 10 of her friends check it out
        for i in range(10):
            self.client.get(f"/posts/{post.id}/", format="json")
        post = Post.objects.get(id=post.id)

        # So it has 10 views
        assert post.views == 10

        # But Sally changes the post, because she spotted a mistake there
        self.client.patch(f"/posts/{post.id}/", {"content": "new_content"})

        # And now she is back to zero
        post = Post.objects.get(id=post.id)
        assert post.views == 0
