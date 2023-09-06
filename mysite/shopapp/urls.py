from django.urls import path
from .views import (
    ShopIndexView,
    GroupsListView,

    ProductDetailsView,
    ProductsListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,

    OrderDetailsView,
    OrdersListView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,

    ProductsDataExportView,
)

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name='index'),
    path("groups/", GroupsListView.as_view(), name='groups_list'),

    path("products/", ProductsListView.as_view(), name='products_list'),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name='product_details'),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name='product_update'),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name='product_delete'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),

    path("products/export/", ProductsDataExportView.as_view(), name='products-export'),

    path("orders/", OrdersListView.as_view(), name='orders_list'),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name='order_details'),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name='order_update'),
    path("orders/<int:pk>/archive/", OrderDeleteView.as_view(), name='order_delete'),
    path("orders/create/", OrderCreateView.as_view(), name='order_create'),

]