from django.urls import path
from .views import PostList, PostListByTag, PostDetail
from .views import PostYearArchiveView
from .views import PostMonthArchiveView
from .views import PostWeekArchiveView
from .views import PostDayArchiveView
from .views import PostTodayArchiveView

app_name = 'blog'
urlpatterns = [
    # post CBVs
    path('list/', PostList.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', PostListByTag.as_view(), name='post_list_by_tag'),
    path('detail/<int:pk>/', PostDetail.as_view(), name='post_detail'),

    path('<int:year>/',
         PostYearArchiveView.as_view(),
         name="post_year_archive"),
    # Example: /2012/08/
    path('<int:year>/<int:month>/',
         PostMonthArchiveView.as_view(month_format='%m'),
         name="archive_month_numeric"),
    # Example: /2012/aug/
    path('<int:year>/<str:month>/',
         PostMonthArchiveView.as_view(),
         name="archive_month"),
    # Example: /2012/week/23/
    path('<int:year>/week/<int:week>/',
         PostWeekArchiveView.as_view(),
         name="archive_week"),
    # Example: /2012/nov/10/
    path('<int:year>/<str:month>/<int:day>/',
         PostDayArchiveView.as_view(),
         name="archive_day"),
    path('today/',
         PostTodayArchiveView.as_view(),
         name="archive_today"),
]
