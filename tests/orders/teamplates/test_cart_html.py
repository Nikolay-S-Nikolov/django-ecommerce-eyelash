from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from lash_store.orders.models import Cart, CartItem
from lash_store.product.models import Product
from decimal import Decimal

UserModel = get_user_model()

class CartTemplateTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email':'user@example.com',
            'password':'pass123'
        }
        self.user = UserModel.objects.create_user(**self.user_data)
        self.product = Product.objects.create(
            name='Продукт',
            price=Decimal('19.99'),
            stock=10,
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.url = reverse('cart_summary')

    def test_template_renders_correctly_with_items(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'orders/cart.html')  # или 'orders/cart.html' ако това е името
        self.assertContains(response, 'Количка')
        self.assertContains(response, self.product.name)
        self.assertContains(response, 'Звършете поръчката')
        self.assertContains(response, f'id="item-{self.cart_item.pk}"')
        self.assertContains(response, f'value="{self.cart_item.quantity}"')
        calculated_price = f"{self.product.price * self.cart_item.quantity:.2f}".replace('.', ',')
        self.assertContains(response, f'{calculated_price}')

    def test_template_renders_empty_cart_message(self):
        self.cart_item.delete()
        self.client.login(**self.user_data)
        response = self.client.get(self.url)
        self.assertContains(response, 'Количката е празна')
        self.assertContains(response, 'Продължи пазаруване')
