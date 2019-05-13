from django import template
from ..models import Post
from django.db.models import Count
from taggit.models import Tag


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.simple_tag
def get_pub_date_list():
    pub_date_list = Post.published.values_list("publish", flat=True)
    pub_date_list = [(item.year, item.month) for item in pub_date_list]
    return set(pub_date_list)


@register.simple_tag
def get_all_tags():
    all_tags = Tag.objects.all()
    return all_tags