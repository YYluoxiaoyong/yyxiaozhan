# -*- coding: utf-8 -*-
# 普通博客列表、详情基类
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# 归档博客列表基类
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import WeekArchiveView
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import TodayArchiveView
# 博客模型引入
from .models import Post, Comment
# 引入标签选择功能
from taggit.models import Tag
from django.shortcuts import get_object_or_404
from django.db.models import Count
# 权限控制
from django.contrib.auth.mixins import LoginRequiredMixin
# 评论操作
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView


# Create your views here.
# 博客列表类视图
class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = 'all_published_posts'
    paginate_by = 4  # if pagination is desired
    ordering = '-publish'
    page_kwarg = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = None
        return context

    def get_queryset(self):
        return Post.published.all()


class PostListByTag(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = 'all_published_posts'
    paginate_by = 4  # if pagination is desired
    ordering = '-publish'
    page_kwarg = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Post.published.filter(tags__in=[self.tag])


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(active=True, post=super().get_object())
        # 显示相近Tag的文章列表
        post_tags_ids = self.object.tags.values_list('id', flat=True)
        similar_tags = Post.published.filter(tags__in=post_tags_ids).exclude(id=self.object.id)
        context['similar_posts'] = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        return context

    def get_object(self):
        obj = super().get_object()
        # 增加额外操作--每访问一次详情页，则浏览次数加1
        obj.explored += 1
        obj.save(update_fields=['explored', ])
        return obj


# 博客年归档
class PostYearArchiveView(LoginRequiredMixin, YearArchiveView):
    queryset = Post.objects.all()
    date_field = "publish"
    make_object_list = True
    allow_future = True


# 博客月归档
class PostMonthArchiveView(LoginRequiredMixin, MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "publish"
    allow_future = True
    template_name = "blog/post_list.html"
    context_object_name = 'all_published_posts'
    paginate_by = 4  # if pagination is desired
    ordering = '-publish'
    page_kwarg = 'page'


# 博客周归档
class PostWeekArchiveView(LoginRequiredMixin, WeekArchiveView):
    queryset = Post.objects.all()
    date_field = "publish"
    week_format = "%W"
    allow_future = True


# 博客日归档
class PostDayArchiveView(LoginRequiredMixin, DayArchiveView):
    queryset = Post.objects.all()
    date_field = "publish"
    allow_future = True


# 博客今日归档
class PostTodayArchiveView(LoginRequiredMixin, TodayArchiveView):
    queryset = Post.objects.all()
    date_field = "publish"
    allow_future = True


# 博文回复
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']
    template_name = 'blog/comment_create.html'
    success_url = '/blog/thanks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.post = self.get_context_data()['target']
        form.instance.author = self.request.user
        return super().form_valid(form)


# 评论回复
class CommentReply(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']
    template_name = 'blog/comment_reply.html'
    success_url = '/blog/thanks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target'] = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.post = self.get_context_data()['target'].post
        form.instance.author = self.request.user
        form.instance.parent_comment = self.get_context_data()['target']
        return super().form_valid(form)


# 感谢页面
class ThanksTemplateView(TemplateView):

    template_name = "blog/thanks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = "评论成功发表！"
        return context
