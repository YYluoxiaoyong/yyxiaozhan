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
from .models import Post
# 引入标签选择功能
from taggit.models import Tag
from django.shortcuts import get_object_or_404
# 权限控制
from django.contrib.auth.mixins import LoginRequiredMixin


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
        print(self.kwargs['tag_slug'])
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Post.published.filter(tags__in=[self.tag])


# 博客详情类视图
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post


# 博客年归档
class PostYearArchiveView(LoginRequiredMixin, YearArchiveView):
    queryset = Post.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = True


# 博客月归档
class PostMonthArchiveView(LoginRequiredMixin, MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "pub_date"
    allow_future = True


# 博客周归档
class PostWeekArchiveView(LoginRequiredMixin, WeekArchiveView):
    queryset = Post.objects.all()
    date_field = "pub_date"
    week_format = "%W"
    allow_future = True


# 博客日归档
class PostDayArchiveView(LoginRequiredMixin, DayArchiveView):
    queryset = Post.objects.all()
    date_field = "pub_date"
    allow_future = True


# 博客今日归档
class PostTodayArchiveView(LoginRequiredMixin, TodayArchiveView):
    queryset = Post.objects.all()
    date_field = "pub_date"
    allow_future = True
