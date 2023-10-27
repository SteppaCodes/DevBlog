from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Tag(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'Draft', 'Draft'
        PUBLISHED = 'Published', 'Published'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=
                               'blog_posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, null=True,  blank=True)
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
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    name = models.CharField(max_length=50)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return self.body
    
