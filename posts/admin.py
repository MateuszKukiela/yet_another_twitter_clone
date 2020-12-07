from django.contrib import admin

from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    search_fields = ("content", "owner")
    list_display = ("id", "content", "owner")


admin.site.register(Post, PostAdmin)
