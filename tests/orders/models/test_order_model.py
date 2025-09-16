from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from lash_store.orders.models import Order, OrderItem
from lash_store.product.models import Product
from lash_store.orders.models import ShippingAddress

UserModel = get_user_model()

class OrderModelTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@example.com',
            password='pass123'
        )
        self.created_product = Product.objects.create(
            name="Test Product",
            description="Some description",
            price=99.99,
            stock=10
        )
        self.created_product_one = Product.objects.create(
            name="Test Product 1",
            description="Some description",
            price=1.00,
            stock=10
        )

    def test__order_creation(self):
        my_order=Order.objects.create(
            customer=self.user,
            total_price=0,
        )

        order_item = OrderItem.objects.create(
            order=my_order,
            product=self.created_product,
            quantity=10,
        )

        expected_total = self.created_product.price * order_item.quantity
        my_order.total_price = expected_total
        my_order.save()

        self.assertEqual(my_order.customer.email, 'test@example.com')
        self.assertEqual(my_order.total_price, 999.90)
        self.assertEqual(str(my_order), f"Поръчка #{my_order.id} - статус: Очаква се")

    def test__calculated_total_price_property(self):
        order = Order.objects.create(customer=self.user, total_price=0)
        OrderItem.objects.create(order=order, product=self.created_product, quantity=2)
        OrderItem.objects.create(order=order, product=self.created_product_one, quantity=1)

        expected_total = 2 * self.created_product.price +  1* self.created_product_one.price
        self.assertEqual(str(order.calculated_total_price), str(expected_total))

    def test__order_str_method(self):
        order = Order.objects.create(customer=self.user, total_price=100)
        self.assertEqual(str(order), f"Поръчка #{order.id} - статус: Очаква се")

        order.status = 'Отменена'
        order.save()
        self.assertEqual(str(order), f"Поръчка #{order.id} - статус: Отменена")

    def test__order_status_and_payment_status_choices(self):
        order = Order.objects.create(
            customer=self.user,
            total_price=100,
            status='Completed',
            payment_status='paid'
        )
        self.assertEqual(order.get_status_display(), 'Завършена')
        self.assertEqual(order.get_payment_status_display(), 'Платена')

    def test__clean_raises_validation_error_for_unpaid_bank_payment(self):
        order = Order.objects.create(
            customer=self.user,
            total_price=100,
            payment_status='unpaid'
        )
        shipping = ShippingAddress.objects.create(
            name='Иван Иванов',
            phone_number='0888123456',
            email='ivan@example.com',
            customer=self.user,
            order=order,
            address='ул. Тестова 1',
            city='София',
            postal_code='9000',
            payment_method='bank_payment'
        )
        order.shippingaddress = shipping
        order.status = 'Completed'
        with self.assertRaises(ValidationError):
            order.clean()

    def test__clean_passes_for_paid_bank_payment(self):
        order = Order.objects.create(
            customer=self.user,
            total_price=100,
            status='Completed',
            payment_status='paid'
        )
        shipping = ShippingAddress.objects.create(
            name='Мария Петрова',
            phone_number='0888123456',
            email='maria@example.com',
            customer=self.user,
            order=order,
            address='ул. Примерна 2',
            city='Пловдив',
            postal_code='4000',
            payment_method='bank_payment'
        )
        order.shippingaddress = shipping
        order.clean()

    def test__email_sent_flag_default(self):
        order = Order.objects.create(customer=self.user, total_price=100)
        self.assertFalse(order.email_sent)

    def test__order_note_field(self):
        note_text = "Моля, доставете след 17:00."
        order = Order.objects.create(customer=self.user, total_price=100, note=note_text)
        self.assertEqual(order.note, note_text)

    def test__order_timestamps(self):
        order = Order.objects.create(customer=self.user, total_price=100)
        self.assertIsNotNone(order.created_at)
        self.assertIsNotNone(order.updated_at)
