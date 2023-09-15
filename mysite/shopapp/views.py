from timeit import default_timer

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend

from myauth.models import Profile
from .models import Product, Order
from .forms import GroupForm

from django.utils.translation import gettext_lazy as _

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import ProductSerializer, OrderSerializer

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 2,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> render:
        context = {
            "form": GroupForm,
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


# Продукты

class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = 'product'


class ProductsListView(ListView):
    template_name = 'shopapp/products_list.html'
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"


class ProductCreateView(CreateView):

    permission_required = ["shopapp.add_product"]

    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy('shopapp:products_list')

    # def form_valid(self, form):
    #
    #     form.instance.created_by = self.request.user
    #     response = super().form_valid(form)
    #     return response


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = "_update_form"

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        self.object = self.get_object()

        has_edit_perm = self.request.user.has_perm("shopapp.change_product")
        created_by_current_user = self.object.created_by == self.request.user
        return has_edit_perm and created_by_current_user

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    search_fields = ["name", "description"]

    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]

    ordering_fields = [
        "name",
        "price",
        "discount",
    ]


# Заказы


class OrderDetailsView(PermissionRequiredMixin, DetailView):

    model = Order
    permission_required = "shopapp.view_order"

    queryset = (Order
                .objects.select_related("user")
                .prefetch_related('products').all()
                )
    context_object_name = 'order'


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects
                .select_related("user")
                .prefetch_related('products')
                )
    context_object_name = 'orders'


class OrderCreateView(CreateView):
    model = Order
    fields = 'user', 'delivery_address', 'promocode'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'user', 'delivery_address', 'promocode'
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:orders_list")


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})


class OrdersDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "created_by": order.user_id,
                # "archived": order.archived,
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    serializer_class = OrderSerializer

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    search_fields = ["pk", "delivery_address"]

    filterset_fields = [
        'delivery_address',
        'promocode',
        'user',
    ]

    ordering_fields = [
        'pk',
        'delivery_address',
        'promocode',
        'user',
    ]