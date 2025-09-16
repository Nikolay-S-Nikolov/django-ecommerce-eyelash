from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from lash_store.orders.models import Order

UserModel = get_user_model()

class OrdersHistoryTemplateTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'user@example.com',
            'password': 'pass123'
        }
        self.user = UserModel.objects.create_user(**self.user_data)
        self.url = reverse('orders_history')

    def test_orders_history_template_with_orders(self):
        order = Order.objects.create(
            customer=self.user,
            total_price=Decimal('49.99'),
            status='Pending',
            created_at=timezone.now()
        )

        self.client.login(**self.user_data)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders_history.html')

        self.assertContains(response, 'История на поръчките')

        self.assertContains(response, f'{order.created_at.strftime("%y%m%d")}-{order.id}')
        self.assertContains(response, order.get_status_display())
        total = f'{order.total_price:.2f}'.replace('.', ',') + ' лв'
        self.assertContains(response, total)

        self.assertContains(response, reverse('order_details', kwargs={'pk': order.pk}))
        self.assertContains(response, 'Детайли')

    def test_orders_history_template_with_no_orders(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders_history.html')

        self.assertContains(response, 'Нямате направени поръчки.')
