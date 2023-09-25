from django.urls import path, include

from rest_framework.routers import DefaultRouter

from django.views.decorators.cache import cache_page

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

    OrdersDataExportView,

    ProductViewSet,
    OrderViewSet,

    UserOrderListsView,
    UserOrdersDataExportView,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name='index'),
    path("groups/", GroupsListView.as_view(), name='groups_list'),

    path("api/", include(routers.urls)),

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

    path("orders/export/", OrdersDataExportView.as_view(), name='orders-export'),

    path("user_orders/<int:user_id>/", UserOrderListsView.as_view(), name='user-orders-list'),
    path("user_orders/<int:user_id>/export/",
         UserOrdersDataExportView.as_view(), name='user-orders-export'),
]