import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from lash_store.orders.models import Cart, CartItem
from lash_store.product.models import Product

UserModel = get_user_model()

class UpdateCartItemQuantityAjaxTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='user@example.com', password='pass123')
        self.product = Product.objects.create(
            name='Продукт',
            description='Описание',
            price=Decimal('19.99'),
            stock=5,
            slug='produkt'
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        self.url = reverse('update_cart_item', args=[self.cart_item.pk])

    def test__redirect_if_not_logged_in(self):
        response = self.client.post(self.url, content_type='application/json', data=json.dumps({'quantity': 1}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
        login_url = reverse('account_login')
        self.assertEqual(data['redirect'], login_url)
        self.assertEqual(data['message'], 'Трябва да сте логнати, за да извършите това действие.')

    def test__quantity_is_updated_successfully(self):
        self.client.login(email='user@example.com', password='pass123')
        response = self.client.post(self.url, content_type='application/json', data=json.dumps({'quantity': 4}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['product_details']['quantity'], 5)
        self.assertEqual(data['product_details']['total_price'], str(Decimal('19.99') * 5))

    def test_quantity_does_not_exceed_stock(self):
        self.client.login(email='user@example.com', password='pass123')
        response = self.client.post(self.url, content_type='application/json', data=json.dumps({'quantity': 10}))
        data = response.json()
        self.assertEqual(data['product_details']['quantity'], self.product.stock)
        self.assertIn('От този продукт може да купите максимум 5 бр.', data['message'])

    def test__quantity_zero_sets_to_one(self):
        self.client.login(email='user@example.com', password='pass123')
        self.assertEqual(self.cart_item.quantity, 1)
        response = self.client.post(self.url, content_type='application/json', data=json.dumps({'quantity': -1}))
        data = response.json()
        self.assertEqual(data['product_details']['quantity'], 1)

    def test__get_request_returns_error(self):
        self.client.login(email='user@example.com', password='pass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Невалидна заявка")
