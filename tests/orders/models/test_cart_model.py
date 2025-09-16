from django.test import TestCase
from django.contrib.auth import get_user_model
from lash_store.orders.models import Cart

UserModel = get_user_model()

class CartModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@example.com',
            password='pass123',
        )

    def test__cart_creation_for_user(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(self.user.cart, cart)

    def test__cart_created_at_is_auto_populated(self):
        cart = Cart.objects.create(user=self.user)
        self.assertIsNotNone(cart.created_at)
        self.assertTrue(hasattr(cart, 'created_at'))
