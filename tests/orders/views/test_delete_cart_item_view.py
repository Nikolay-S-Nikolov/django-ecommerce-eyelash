from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from lash_store.orders.models import Cart, CartItem
from lash_store.product.models import Product
from decimal import Decimal

UserModel = get_user_model()

class DeleteCartItemViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='user@example.com',
            password='pass123',
        )
        self.other_user = UserModel.objects.create_user(
            email='other@example.com',
            password='pass123',
        )
        self.product = Product.objects.create(
            name='Продукт',
            description='Описание',
            price=Decimal('19.99'),
            stock=100,
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )
        self.url = reverse('delete_cart_item', args=[self.cart_item.pk])

    def test__redirect_if_not_logged_in(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test__delete_cart_item_successfully(self):
        self.client.login(email='user@example.com', password='pass123')
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse('cart_summary'))
        self.assertFalse(CartItem.objects.filter(pk=self.cart_item.pk).exists())

        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно премахнат" in str(m) for m in messages_list))

    def test__user_cannot_delete_other_users_cart_item(self):
        self.client.login(email='other@example.com', password='pass123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test__invalid_cart_item_pk_returns_404(self):
        self.client.login(email='user@example.com', password='pass123')
        invalid_url = reverse('delete_cart_item', args=[9999])
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, 404)
