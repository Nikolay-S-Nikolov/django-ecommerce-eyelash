from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from lash_store.orders.models import Cart, CartItem
from lash_store.product.models import Product
from decimal import Decimal

UserModel = get_user_model()

class CheckoutTemplateTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'user@example.com',
            'password':'pass123'
        }
        self.user = UserModel.objects.create_user(**self.user_data)
        self.product = Product.objects.create(
            name='Продукт',
            price=Decimal('19.99'),
            stock=10
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.url = reverse('checkout')

    def test_checkout_template_renders_correctly(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/checkout.html')

        self.assertContains(response, 'Завършване на поръчката')

        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="phone_number"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="address"')
        self.assertContains(response, 'name="city"')
        self.assertContains(response, 'name="postal_code"')
        self.assertContains(response, 'name="note"')

        self.assertContains(response, self.product.name)
        self.assertContains(response, f'Количество: {self.cart_item.quantity} бр.')
        calculated_price = f"{self.product.price * self.cart_item.quantity:.2f}".replace('.', ',')
        self.assertContains(response, f'{calculated_price}')

        self.assertContains(response, 'value="pay_on_delivery"')
        self.assertContains(response, 'value="bank_payment"')

        self.assertContains(response, 'type="submit"')
        self.assertContains(response, 'Поръчай')
