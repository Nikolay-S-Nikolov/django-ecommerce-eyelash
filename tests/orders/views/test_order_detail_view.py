from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from lash_store.orders.models import Order
from decimal import Decimal

UserModel = get_user_model()

class OrderDetailViewTest(TestCase):
    def setUp(self):
        self.user_data = {'email': 'user@example.com', 'password': 'pass123'}
        self.other_user_data = {'email': 'other@example.com', 'password': 'pass456'}

        self.user = UserModel.objects.create_user(**self.user_data)
        self.other_user = UserModel.objects.create_user(**self.other_user_data)

        self.order = Order.objects.create(customer=self.user, total_price=Decimal('39.99'), status='Pending')
        self.other_order = Order.objects.create(customer=self.other_user, total_price=Decimal('99.99'), status='Delivered')

        self.url = reverse('order_details', kwargs={'pk': self.order.pk})
        self.other_url = reverse('order_details', kwargs={'pk': self.other_order.pk})

    def test__redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test__order_detail_view_renders_template_and_context(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_details.html')
        self.assertEqual(response.context['order'], self.order)

    def test__user_cannot_access_other_users_order(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.other_url)
        self.assertEqual(response.status_code, 404)  # защото get_queryset филтрира по user
