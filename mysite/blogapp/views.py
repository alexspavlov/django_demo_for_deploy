from django.views.generic import ListView

from .models import Article


class BlogListView(ListView):

    queryset = (
        Article.objects
        .select_related("author")
        .prefetch_related("tags")
        .defer("bio")
    )

    template_name = 'blogapp/articles_list.html'
    context_object_name = "articles"
