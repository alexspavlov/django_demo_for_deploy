from django.urls import path, include

from .views import BlogListView

app_name = "blogapp"


urlpatterns = [
    path('', BlogListView.as_view(), name='posts_list')
]