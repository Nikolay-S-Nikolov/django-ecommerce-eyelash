from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from lash_store.orders.models import Order, OrderItem
from lash_store.product.models import Product

UserModel = get_user_model()

class OrderItemModelTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@example.com',
            password='pass123',
        )
        self.product = Product.objects.create(
            name='Продукт',
            description='Описание',
            price=Decimal('19.99'),
            stock=50,
        )
        self.order = Order.objects.create(
            customer=self.user,
            total_price=0,
        )

    def test__price_property_returns_correct_value(self):
        item = OrderItem(
            order=self.order,
            product=self.product,
            quantity=3,
        )
        expected_price = Decimal('59.97')
        self.assertEqual(item.price, expected_price)

    def test__saved_price_is_calculated_on_save(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )
        expected_saved_price = Decimal('39.98')
        self.assertEqual(item.saved_price, expected_saved_price)

    def test__str_method_returns_meaningful_string(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )
        expected_str = f"Поръчани 1 бр. от Продукт"
        self.assertEqual(str(item), expected_str)

    def test__quantity_can_be_zero(self):
        order_item=OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=0,
        )
        self.assertEqual(order_item.quantity, 0)

    def test__order_item_links_to_order_and_product(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )
        self.assertEqual(item.order, self.order)
        self.assertEqual(item.product, self.product)