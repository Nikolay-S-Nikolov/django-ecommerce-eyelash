from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from lash_store.orders.models import Order
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

UserModel = get_user_model()

class OrderHistoryViewTest(TestCase):
    def setUp(self):
        self.user_data = {'email':'user@example.com', 'password':'pass123'}
        self.other_user_data = {'email':'other@example.com', 'password':'pass456'}

        self.user = UserModel.objects.create_user(**self.user_data)
        self.other_user = UserModel.objects.create_user(**self.other_user_data)

        self.order1 = Order.objects.create(customer=self.user, total_price=Decimal('20.00'), status='Pending', created_at=timezone.now())
        self.order2 = Order.objects.create(customer=self.user, total_price=Decimal('40.00'), status='Processing', created_at=timezone.now() + timedelta(minutes=1))

        self.order_other = Order.objects.create(customer=self.other_user, total_price=Decimal('99.99'), status='Delivered')

        self.url = reverse('orders_history')

    def test__redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test__order_history_view_renders_template_and_context(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders_history.html')
        self.assertIn('orders', response.context)

    def test__only_user_orders_are_displayed(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.url)
        orders = response.context['orders']
        self.assertEqual(len(orders), 2)
        self.assertNotIn(self.order_other, orders)
        self.assertEqual(orders[0].status, 'Processing')
        self.assertEqual(orders[0].get_status_display(), 'В обработка')

    def test__orders_are_sorted_by_created_at_desc(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.url)
        orders = response.context['orders']
        self.assertEqual(orders[0], self.order2)
        self.assertEqual(orders[1], self.order1)
