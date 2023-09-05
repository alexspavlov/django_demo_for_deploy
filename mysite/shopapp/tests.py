from random import choices
from string import ascii_letters

from django.conf import settings

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    # def test_create_product(self):
    #     response = self.client.post(
    #         reverse("shopapp:product_create"),
    #         {
    #             "created_by": "john",
    #             "name": self.product_name,
    #             "price": "123.45",
    #             "description": "A good table",
    #             "discount": "10",
    #         },
    #         HTTP_USER_AGENT='Mozilla/5.0'
    #     )
    #     self.assertRedirects(response, reverse("shopapp:products_list"))
    #     self.assertTrue(
    #         Product.objects.filter(name=self.product_name).exists()
    #     )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDown(cls):
        cls.product.delete()

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk}),
            HTTP_USER_AGENT='Mozilla/5.0'
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'products-fixture.json',
        'orders-fixture.json',
    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"), HTTP_USER_AGENT='Mozilla/5.0')

        products = Product.objects.filter(archived=False).all()
        products_ = response.context["products"]
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products_list.html')


class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='bob', password='1234')
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)