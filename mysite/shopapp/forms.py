from django import forms
from django.core import validators
from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount'

    # name = forms.CharField(label='Name', max_length=100)
    # price = forms.DecimalField(label='Price', min_value=1, max_value=100000000, decimal_places=2)
    # description = forms.CharField(
    #     label='Description',
    #     widget=forms.Textarea(attrs={"rows": "5", "cols": "30"}),
    #     validators=[validators.RegexValidator(
    #         regex=r'great',
    #         message="Field must contain word 'great'"
    #     )],
    # )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'user', 'delivery_address', 'promocode'
