from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _


def product_preview_directly_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    """
    Модель Product представляет товар, который можно
    продавать в Интернет-магазине.

    Заказы тут: :model:`shopapp.Order`
    """
    class Meta:
        ordering = ['name']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directly_path)

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})"

    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + '...'

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"


class Order(models.Model):
    """
    Модель Order представляет заказ, который можно
    сделать в Интернет-магазине.

    Товары тут: :model:`shopapp.Product`
    """
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")

    receipt = models.FileField(null=True, upload_to='orders/receipts/')

    def __str__(self) -> str:
        return f"Order(pk={self.pk})"
