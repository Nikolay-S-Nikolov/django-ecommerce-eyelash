from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from lash_store.orders.models import Cart, CartItem, Order, OrderItem
from lash_store.product.models import Product
from decimal import Decimal

UserModel = get_user_model()

class CheckoutViewTest(TestCase):
    def setUp(self):
        self.user_data={
            'email' : 'user@example.com',
            'password' : 'pass123'
        }
        self.user = UserModel.objects.create_user(**self.user_data)
        self.product = Product.objects.create(
            name='Тестов продукт',
            description='Описание',
            price=Decimal('19.99'),
            stock=100,
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.url = reverse('checkout')

        self.form_data = {
            'name': 'Иван Иванов',
            'phone_number': '0888123456',
            'email': 'ivan@example.com',
            'address': 'ул. Тестова 1',
            'city': 'София',
            'postal_code': '1000',
            'payment_method': 'pay_on_delivery',
            'note': 'Моля, доставете след 17:00.'
        }

    def test__redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test__redirect_if_cart_is_empty(self):
        self.cart_item.delete()
        self.client.login(**self.user_data)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse('cart_summary'))
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Вашата количка е празна" in str(m) for m in messages_list))

    def test__checkout_view_renders_correct_template(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'orders/checkout.html')
        self.assertIn('cart_items', response.context)
        self.assertEqual(response.context['total'], Decimal('39.98'))

    def test__form_valid_creates_order_and_order_items(self):
        self.client.login(**self.user_data)
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertRedirects(response, reverse('order_confirmation', kwargs={'pk': Order.objects.first().pk}))
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertFalse(CartItem.objects.filter(cart=self.cart).exists())

        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Поръчката е изпратена" in str(m) for m in messages_list))

    def test_unit_sold_increases_quantity(self):
        self.client.login(**self.user_data)
        self.client.post(self.url, data=self.form_data)
        self.product.refresh_from_db()
        self.assertEqual(self.product.units_sold, 2)


