import json
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from lash_store.orders.models import CartItem
from lash_store.product.models import Product

UserModel = get_user_model()

class AddToCartAjaxTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='user@example.com',
            password='pass123',
        )
        self.product = Product.objects.create(
            name='Тестов продукт',
            description='Описание',
            price=Decimal('19.99'),
            stock=5,
            slug='testov-produkt'
        )
        self.url = reverse('add_to_cart', args=[self.product.id])

    def test__redirect_if_not_logged_in(self):
        login_url = reverse('account_login')
        response = self.client.post(self.url, content_type='application/json', data=json.dumps({'quantity': 1}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['redirect'], login_url)
        self.assertEqual(data['message'], 'Трябва да сте логнати, за да извършите това действие.')

    def test__add_product_to_cart_successfully(self):
        self.client.login(email='user@example.com', password='pass123')
        response = self.client.post(self.url, content_type='application/json', data=json.dumps({'quantity': 2}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['product_details']['quantity'], 2)
        self.assertEqual(data['product_details']['name'], self.product.name)

    def test__quantity_does_not_exceed_stock(self):
        self.client.login(email='user@example.com', password='pass123')

        response = self.client.post(self.url, content_type='application/json', data=json.dumps({'quantity': 10}))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['product_details']['quantity'], self.product.stock)
        self.assertEqual( data['message'], 'От този продукт може да купите максимум 5 бр.')

    def test__add_same_product_twice_accumulates_quantity(self):
        self.client.login(email='user@example.com', password='pass123')
        self.client.post(self.url, content_type='application/json', data=json.dumps({'quantity': 2}))
        self.client.post(self.url, content_type='application/json', data=json.dumps({'quantity': 1}))
        item = CartItem.objects.get(cart__user=self.user, product=self.product)
        self.assertEqual(item.quantity, 3)

    def test__method_get_returns_error(self):
        self.client.login(email='user@example.com', password='pass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Невалидна заявка")
