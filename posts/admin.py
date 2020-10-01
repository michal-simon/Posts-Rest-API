from django.contrib import admin

from posts.models import PostLike, Post

admin.site.register(Post)
admin.site.register(PostLike)
