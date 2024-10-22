from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.functions import Now
from taggit.managers import TaggableManager
from django.contrib.auth.models import User




class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    total_likes = models.PositiveIntegerField(default=0)
    # publish = models.DateTimeField(default=timezone.now)
    publish = models.DateTimeField(db_default=Now())    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField()
    tags = TaggableManager()
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.PUBLISHED
    )   

    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='blogs_liked',
        blank=True
    )
    
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
            models.Index(fields=['-total_likes']),
        ]
    
    
    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day, 
                self.slug
            ]
    )
        

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'