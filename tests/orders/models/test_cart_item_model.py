from django.test import TestCase
from django.contrib.auth import get_user_model
from lash_store.orders.models import Cart, CartItem
from lash_store.product.models import Product

UserModel = get_user_model()

class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@example.com',
            password='pass123',
        )
        self.cart = Cart.objects.create(user=self.user)
        self.product = Product.objects.create(
            name='Продукт',
            description='Описание',
            price=19.99,
            stock=100,
        )

    def test__cart_item_creation_and_association(self):
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=3,
        )

        self.assertEqual(item.cart, self.cart)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 3)

    def test__cart_item_str_method(self):
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(str(item), "2 x Продукт in cart")

    def test__cart_item_default_quantity(self):
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
        )
        self.assertEqual(item.quantity, 1)
