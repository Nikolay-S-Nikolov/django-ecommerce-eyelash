from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from lash_store.orders.models import Cart, CartItem
from lash_store.product.models import Product
from decimal import Decimal

UserModel = get_user_model()

class CartSummaryViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='user@example.com',
            password='pass123',
        )
        self.product1 = Product.objects.create(
            name='Продукт 1',
            description='Описание',
            price=Decimal('10.00'),
            stock=100,
        )
        self.product2 = Product.objects.create(
            name='Продукт 2',
            description='Описание',
            price=Decimal('20.00'),
            stock=100,
        )
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=self.cart,
            product=self.product1,
            quantity=2,
        )
        CartItem.objects.create(
            cart=self.cart,
            product=self.product2,
            quantity=1,
        )

    def test__cart_summary_view_requires_login(self):
        response = self.client.get(reverse('cart_summary'))
        self.assertEqual(response.status_code, 302)


    def test__cart_summary_view_returns_correct_items(self):
        self.client.login(email='user@example.com', password='pass123')
        response = self.client.get(reverse('cart_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/cart.html')
        self.assertEqual(len(response.context['object_list']), 2)

    def test__cart_summary_total_is_correct(self):
        self.client.login(email='user@example.com', password='pass123')
        response = self.client.get(reverse('cart_summary'))
        self.assertEqual(response.context['total'], Decimal('40.00'))
