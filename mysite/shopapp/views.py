from timeit import default_timer
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.urls import reverse

from .models import Product, Order
from .forms import ProductForm, OrderForm


def shop_index(request: HttpRequest) -> render:
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]

    context = {
        "time_running": default_timer(),
        "products": products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest) -> render:
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)


def products_list(request: HttpRequest) -> render:
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'shopapp/products_list.html', context=context)


def orders_list(request: HttpRequest) -> render:
    context = {
        "orders": Order.objects.all(),
        # "orders": Order.objects.select_related("user").prefetch_related('products').all(),
    }
    return render(request, 'shopapp/orders_list.html', context=context)


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Product.objects.create(**form.cleaned_data)
            url = reverse('shopapp:products_list')
            return redirect(url)
    else:
        form = ProductForm()
    context = {
        "form": form,
    }
    return render(request, 'shopapp/create-product.html', context=context)


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            # Product.objects.create(**form.cleaned_data)
            url = reverse('shopapp:orders_list')
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        "form": form,
    }
    return render(request, 'shopapp/create-order.html', context=context)