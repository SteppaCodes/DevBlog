from django.contrib import admin
from apps.blog.models import Post, Comment,Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)