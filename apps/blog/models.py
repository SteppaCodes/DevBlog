from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'Draft', 'Draft'
        PUBLISHED = 'Published', 'Published'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=
                               'blog_posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    status = models.CharField(choices=Status.choices, default=Status.DRAFT,max_length=10)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager() #Always add the default manager when you create a custom one
    published = PublishedManager()


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

    def __str__(self):
        return self.title
    
