from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path

from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin

from .forms import CSVImportForm


@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


class OrderInline(admin.TabularInline):
    model = Product.orders.through
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "shopapp/products_changelist.html"

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        form = CSVImportForm()
        context = {
            "form": form,
        }
        return render(request, "admin/csv_form.html", context)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]
        return new_urls + urls

    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = '-name', 'pk'
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('wide', 'collapse',),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': "Extra options. Field 'archived' is for soft delete. "
        })
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        else:
            return obj.description[:48] + '...'

    description_short.short_description = "My Custom Field"


# admin.site.register(Product, ProductAdmin)


class ProductInline(admin.StackedInline):
    model = Order.products.through
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
