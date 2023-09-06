from random import choices
from string import ascii_letters

from django.conf import settings

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


# class ProductCreateViewTestCase(TestCase):
#
#     @classmethod
#     def setUp(cls):
#         cls.product = Product.objects.create(name="Best Product")
#
#     def test_create_product(self):
#         response = self.client.post(
#             reverse("shopapp:product_create"),
#             {
#                 "created_by": "john",
#                 "name": self.product.name,
#                 "price": "123.45",
#                 "description": "A good table",
#                 "discount": "10",
#             },
#             HTTP_USER_AGENT='Mozilla/5.0'
#         )
#         self.assertRedirects(response, reverse("shopapp:products_list"))
#         self.assertTrue(
#             Product.objects.filter(name=self.product.name).exists()
#         )


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


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'products-fixture.json',
        'orders-fixture.json',
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
            HTTP_USER_AGENT='Mozilla/5.0',
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]

        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='Jack', password='qwerty')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        permission = Permission.objects.get(codename="view_order")
        self.user.user_permissions.add(permission)
        self.order = Order.objects.create(
            delivery_address='Test address',
            promocode='Test promocode',
            user=self.user,
        )

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_details",
                    kwargs={"pk": self.order.pk}),
            HTTP_USER_AGENT='Mozilla/5.0',
        )
        self.assertContains(response, self.order.delivery_address)


class OrdersExportViewTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'products-fixture.json',
        'orders-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='Jack',
            password='qwerty',
            is_staff=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_orders_view(self):

        response = self.client.get(
            reverse("shopapp:orders-export"),
            HTTP_USER_AGENT='Mozilla/5.0',
        )

        self.assertEqual(response.status_code, 200)

        orders = Order.objects.order_by("pk").all()

        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "created_by": order.user_id,
                # "archived": order.archived,
            }
            for order in orders
        ]

        received_data = response.json
        print("received data: ", received_data)
        print("expected data: ", expected_data)

        orders_data = response.json()
        self.assertEqual(
            orders_data["orders"],
            expected_data,
        )
