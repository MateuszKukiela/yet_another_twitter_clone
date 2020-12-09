from django.contrib.auth.models import User
from django.test import TestCase

from posts.models import Post


class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.post = Post(id=1, content="test_content", owner=self.user)

    def test_model_can_create_a_post(self):

        old_count = Post.objects.count()
        self.post.save()
        new_count = Post.objects.count()
        self.assertNotEqual(old_count, new_count)

        # assert post has 0 views
        self.assertEqual(self.post.views, 0)
