from tkinter.font import names

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from lash_store.product.models import Product, ProductImages

UserModel=get_user_model()

class ProductModelTest(TestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test_user@user,com',
            'password':'123qWER'
        }
        self.user = UserModel.objects.create(**self.user_data)

    def test__product_creation(self):
        product = Product.objects.create(
            name="Test Product",
            description="Some description",
            price=99.99,
            stock=10
        )
        self.assertEqual(product.slug,"test-product")
        self.assertEqual(str(product), "Test Product")

    def test__unique_name_constraint__raises_validation_error(self):
        Product.objects.create(name="Unique test", description="desc", price=10, stock=1)
        new_product = Product(name="Unique test", slug="unique-test", description="desc", price=20.2323, stock=12)

        with self.assertRaises(ValidationError) as ve:
            new_product.full_clean()

        error_dict = ve.exception.message_dict

        self.assertIn('name', error_dict)
        self.assertIn('Продукт с това име вече съществува.', error_dict['name'])

        # Пример: проверка дали има грешка за 'slug'
        self.assertIn('slug', error_dict)
        self.assertIn('Product с този Slug вече съществува.', error_dict['slug'])

        self.assertIn('price', error_dict)
        self.assertIn('Уверете се, че има не повече от 2 знака след десетичната запетая.', error_dict['price'])

    def test__product_image_relation(self):
        product = Product.objects.create(name="Camera", description="desc", price=100, stock=5)
        image = ProductImages.objects.create(product=product, image="products/test.jpg")
        self.assertEqual(image.product, product)
        self.assertEqual( str(image), "Image for Camera")
        self.assertEqual(str(product), "Camera")

