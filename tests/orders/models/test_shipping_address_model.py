from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from lash_store.orders.models import Order, ShippingAddress
from lash_store.product.models import Product
from decimal import Decimal

UserModel = get_user_model()

class ShippingAddressModelTest(TestCase):
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
        self.order = Order.objects.create(
            customer=self.user,
            total_price=Decimal('59.97'),
        )

    def test__valid_shipping_address_creation(self):
        address = ShippingAddress.objects.create(
            name='Иван Иванов',
            phone_number='0888123456',
            email='ivan@example.com',
            customer=self.user,
            order=self.order,
            address='ул. Тестова 1',
            city='София',
            postal_code='9000',
            payment_method='pay_on_delivery'
        )
        self.assertEqual(address.name, 'Иван Иванов')
        self.assertEqual(address.phone_number, '0888123456')
        self.assertEqual(address.email, 'ivan@example.com')
        self.assertEqual(address.address, 'ул. Тестова 1')
        self.assertEqual(address.postal_code, '9000')
        self.assertEqual(address.city, 'София')
        self.assertEqual(address.payment_method, 'pay_on_delivery')
        self.assertEqual(address.customer, self.user)
        self.assertEqual(address.order, self.order)


    def test__str_method_returns_expected_string(self):
        address = ShippingAddress.objects.create(
            name='Мария Петрова',
            phone_number='0888123456',
            email='maria@example.com',
            customer=self.user,
            order=self.order,
            address='ул. Примерна 2',
            city='Пловдив',
            postal_code='4000',
            payment_method='bank_payment'
        )
        expected_str = f"Адрес за доставка за {self.order}"
        self.assertEqual(str(address), expected_str)

    def test__invalid_phone_number_raises_validation_error(self):
        address = ShippingAddress(
            name='Грешен Номер',
            phone_number='123456',
            email='invalid@example.com',
            customer=self.user,
            order=self.order,
            address='ул. Грешна',
            city='Варна',
            postal_code='9000',
            payment_method='pay_on_delivery'
        )
        with self.assertRaises(ValidationError):
            address.full_clean()

    def test__valid_phone_number_passes_validation(self):
        address = ShippingAddress(
            name='Валиден Номер',
            phone_number='+359899123456',
            email='valid@example.com',
            customer=self.user,
            order=self.order,
            address='ул. Валидна',
            city='Русе',
            postal_code='7000',
            payment_method='bank_payment'
        )
        try:
            address.full_clean()
        except ValidationError:
            self.fail("Валиден телефонен номер даде ValidationError")

    def test__payment_method_choices_set_correctly(self):
        address = ShippingAddress.objects.create(
            name='Плащане 2',
            phone_number='0888123456',
            email='pay2@example.com',
            customer=self.user,
            order=self.order,
            address='ул. Плащане 2',
            city='София',
            postal_code='1000',
            payment_method='bank_payment'
        )
        self.assertEqual(address.get_payment_method_display(), 'Банков превод')
