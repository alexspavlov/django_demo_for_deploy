from django.urls import path, include

from .views import BlogListView, BlogDetailView, LatestArticlesFeed

app_name = "blogapp"


urlpatterns = [
    path('', BlogListView.as_view(), name='posts_list'),
    path('articles/<int:pk>/', BlogDetailView.as_view(), name='post_details'),
    path('latest/feed/', LatestArticlesFeed(), name='posts_feed')
]