from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    CATEGORY_CHOICES = (('beijing', '北京'), ('shanghai', '上海'), ('guangzhou', '广州'), ('shenzhen', '深圳'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    # 点赞功能
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio:image_detail', args=[self.pk])

