import factory
from faker import Factory

from django.contrib.auth.models import User
from posts.models import Post


faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user_%d" % n)
    password = factory.Sequence(lambda n: "password_%d" % n)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    owner = factory.SubFactory(UserFactory)
    content = faker.text(max_nb_chars=160)
