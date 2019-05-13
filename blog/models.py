from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
# 自定义published管理器
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


# 博客模型
class Post(models.Model):
    STATUS_CHOICES = (('draft', '草稿态'), ('published', '发布态'))

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    body = RichTextUploadingField(default='请在这里输入博客正文')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    explored = models.PositiveIntegerField(db_index=True, default=0)  # 计算博客访问量
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    objects = models.Manager()  # 默认的管理器
    published = PublishedManager()  # 自定义管理器

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.pk])

    tags = TaggableManager()


# 评论模型
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children_comments', null=True)
    body = RichTextUploadingField(default='发表您的评论')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.post)
