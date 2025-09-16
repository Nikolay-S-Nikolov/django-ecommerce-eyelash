from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from lash_store.orders.models import Order, ShippingAddress
from decimal import Decimal

UserModel = get_user_model()

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class OrderConfirmationViewTest(TestCase):
    def setUp(self):
        self.user_data={
            'email' : 'user@example.com',
            'password' : 'pass123'
        }
        self.user = UserModel.objects.create_user(**self.user_data)
        self.order = Order.objects.create(customer=self.user, total_price=Decimal('39.98'), status='Pending')
        self.shipping = ShippingAddress.objects.create(
            name='Иван Иванов',
            phone_number='0888123456',
            email='ivan@example.com',
            customer=self.user,
            order=self.order,
            address='ул. Тестова 1',
            city='София',
            postal_code='1000',
            payment_method='pay_on_delivery'
        )
        self.url = reverse('order_confirmation', kwargs={'pk': self.order.pk})

    def test__redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test__order_confirmation_view_renders_template_and_context(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_confirmation.html')
        self.assertEqual(response.context['order'], self.order)

    def test__confirmation_email_is_sent_once(self):
        self.client.login(**self.user_data)
        self.assertFalse(self.order.email_sent)

        self.client.get(self.url)
        self.order.refresh_from_db()

        self.assertTrue(self.order.email_sent)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Потвърждение за поръчка", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, [self.shipping.email])

    def test__email_not_sent_if_already_marked_sent(self):
        self.client.login(**self.user_data)
        self.order.email_sent = True
        self.order.save(update_fields=['email_sent'])

        self.client.get(self.url)

        self.assertEqual(len(mail.outbox), 0)
