from functools import total_ordering
from unittest import expectedFailure

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from lash_store.orders.models import Order, OrderItem, ShippingAddress
from lash_store.product.models import Product

UserModel = get_user_model()

class OrderConfirmationTemplateTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'user@example.com',
            'password': 'pass123'
        }
        self.user = UserModel.objects.create_user(**self.user_data)
        self.product = Product.objects.create(
            name='Продукт',
            price=Decimal('19.99'),
            stock=10,
        )
        self.order = Order.objects.create(
            customer=self.user,
            total_price=Decimal('39.98'),
            status='Pending',
            payment_status='Unpaid',
            created_at=timezone.now(),
            note='Моля, доставете след 17:00.'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            saved_price=Decimal('39.98')
        )
        self.shipping = ShippingAddress.objects.create(
            order=self.order,
            customer=self.user,
            name='Иван Иванов',
            address='ул. Тестова 1',
            city='София',
            postal_code='1000',
            email='ivan@example.com',
            phone_number='0888123456',
            payment_method='pay_on_delivery'
        )

        self.url = reverse('order_confirmation', kwargs={'pk': self.order.pk})

    def test_order_confirmation_template_renders_correctly(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_confirmation.html')

        self.assertContains(response, 'Вашата поръчка е изпратена за обработка')
        self.assertContains(response, f'Поръчка № {self.order.created_at.strftime("%y%m%d")}-{self.order.id}')

        self.assertContains(response, self.order.get_status_display())
        self.assertContains(response, self.order.get_payment_status_display())

        self.assertContains(response, self.product.name)
        self.assertContains(response, f'Количество: {self.order_item.quantity} бр.')
        expected =  f'{self.order_item.saved_price:.2f}'.replace('.', ',') + ' лв'
        self.assertContains(response,expected)

        total = f'{self.order.total_price:.2f}'.replace('.', ',') + ' лв'
        self.assertContains(response, total)

        self.assertContains(response, self.shipping.name)
        self.assertContains(response, self.shipping.address)
        self.assertContains(response, self.shipping.city)
        self.assertContains(response, self.shipping.postal_code)
        self.assertContains(response, self.shipping.email)
        self.assertContains(response, self.shipping.phone_number)
        self.assertContains(response, self.order.note)

        self.assertContains(response, reverse('orders_history'))
        self.assertContains(response, reverse('products'))
