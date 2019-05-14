# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from .models import Image


# Create your views here.
class ImageList(ListView):

    model = Image
    template_name = "portfolio/image_list.html"
    paginate_by = 8  # 8个图片为一页


class ImageDetail(DetailView):

    model = Image
    template_name = "portfolio/image_detail.html"

