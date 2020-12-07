from django.db import models


class Post(models.Model):
    content = models.CharField(
        max_length=160,
        blank=False,
        help_text="Text content of the post. Max 160 characters",
    )
    views = models.IntegerField(default=0)
    owner = models.ForeignKey(
        "auth.User",
        related_name="posts",
        on_delete=models.CASCADE,
        help_text="Original poster",
    )
