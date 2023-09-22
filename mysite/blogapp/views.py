from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView

from .models import Article


class BlogListView(ListView):
    queryset = (
        Article.objects
        .filter(pub_date__isnull=False)
        .order_by("-pub_date")
    )

    template_name = 'blogapp/articles_list.html'
    context_object_name = "articles"


class BlogDetailView(DetailView):
    model = Article

    template_name = "blogapp/article_details.html"
    context_object_name = "article"


class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and addition blog articles"
    link = reverse_lazy("blogapp:posts_list")

    def items(self):
        return (
            Article.objects
            .filter(pub_date__isnull=False)
            .order_by("-pub_date")[:5]
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.body[:200]

    def item_link(self, item: Article):
        return reverse("blogapp:post_details", kwargs={"pk": item.pk})
