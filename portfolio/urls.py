from django.urls import path
from .views import ImageList, ImageDetail

app_name = 'portfolio'
urlpatterns = [
    # image CBVs
    path('image/list/', ImageList.as_view(), name='image_list'),
    path('image/detail/<int:pk>/', ImageDetail.as_view(), name='image_detail'),
]
