from django.test import TestCase
from django.contrib.auth import get_user_model
from lash_store.orders.forms import CheckoutForm
from lash_store.orders.models import Cart, CartItem, Order, ShippingAddress
from lash_store.product.models import Product
from decimal import Decimal

UserModel = get_user_model()

class CheckoutFormTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@example.com',
            password='pass123',
        )
        self.product = Product.objects.create(
            name='Продукт',
            description='Описание',
            price=Decimal('19.99'),
            stock=100,
        )
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.valid_data = {
            'name': 'Иван Иванов',
            'phone_number': '0888123456',
            'email': 'ivan@example.com',
            'address': 'ул. Тестова 1',
            'city': 'София',
            'postal_code': '1000',
            'payment_method': 'pay_on_delivery',
            'note': 'Моля, доставете след 17:00.'
        }

    def test_form_is_valid_with_correct_data(self):
        form = CheckoutForm(data=self.valid_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_wrong_phone_number(self):
        self.valid_data['phone_number'] = '123456'
        form = CheckoutForm(data=self.valid_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_form_invalid_with_wrong_postal_code(self):
        self.valid_data['postal_code'] = '123'
        form = CheckoutForm(data=self.valid_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('postal_code', form.errors)

    def test_clean_method_raises_error_if_cart_missing(self):
        user_without_cart = UserModel.objects.create_user(
            email='no_cart@example.com',
            password='pass123',
        )
        form = CheckoutForm(data=self.valid_data, user=user_without_cart)
        self.assertFalse(form.is_valid())

    def test_clean_method_sets_total_price_and_status(self):
        form = CheckoutForm(data=self.valid_data, user=self.user)
        form.is_valid()
        cleaned = form.clean()
        self.assertEqual(cleaned['status'], 'Pending')
        self.assertEqual(cleaned['total_price'], Decimal('39.98'))

    def test_save_creates_order_and_shipping_address(self):
        form = CheckoutForm(data=self.valid_data, user=self.user)
        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertIsInstance(order, Order)
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.total_price, Decimal('39.98'))

        shipping = ShippingAddress.objects.get(order=order)
        self.assertEqual(shipping.name, self.valid_data['name'])
        self.assertEqual(shipping.city, self.valid_data['city'])

    def test_prepopulate_fields_from_last_order(self):
        ShippingAddress.objects.create(
            name='Мария Петрова',
            phone_number='0899123456',
            email='maria@example.com',
            customer=self.user,
            order=Order.objects.create(customer=self.user, total_price=10),
            address='ул. Примерна',
            city='Пловдив',
            postal_code='4000',
            payment_method='bank_payment'
        )
        form = CheckoutForm(user=self.user)
        self.assertEqual(form.fields['name'].initial, 'Мария Петрова')
        self.assertEqual(form.fields['city'].initial, 'Пловдив')
