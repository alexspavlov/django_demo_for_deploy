from django.db import models

from django.urls import reverse, reverse_lazy


class Author(models.Model):
    name = models.CharField(max_length=100),
    bio = models.TextField(null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=40)


class Tag(models.Model):
    name = models.CharField(max_length=20)


class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    pub_date = models.DateField()
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag)

    def get_absolute_url(self):
        return reverse("blogapp:post_details", kwargs={"pk": self.pk})


