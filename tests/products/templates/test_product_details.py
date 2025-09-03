from django.test import TestCase
from django.urls import reverse
from lash_store.product.models import Product, ProductImages

class ProductDetailTemplateTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Lash Fan",
            description="Ръчно изработени ветрила",
            price=25.00,
            stock=8
        )
        ProductImages.objects.create(product=self.product, image="products/img1.jpg")
        ProductImages.objects.create(product=self.product, image="products/img2.jpg")

    def test__detail_view_renders_correct_template(self):
        response = self.client.get(reverse('product_details', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_detail.html')

    def test__product_data_is_displayed(self):
        response = self.client.get(reverse('product_details', kwargs={'slug': self.product.slug}))
        html = response.content.decode('utf-8')

        self.assertIn(self.product.name, html)
        self.assertIn("Ръчно изработени ветрила", html)
        self.assertIn("Добави в количката", html)
        self.assertIn("Изберете количество", html)
        self.assertIn(f"Остават само {self.product.stock} броя", html)

        expected_price = f"Цена: {self.product.price:.2f}".replace('.', ',') + " лв"
        self.assertIn(expected_price, html)

    def test__images_are_rendered(self):
        response = self.client.get(reverse('product_details', kwargs={'slug': self.product.slug}))
        html = response.content.decode('utf-8')

        first_image_url = self.product.images.first().image.url
        last_image_url = self.product.images.last().image.url

        self.assertIn(first_image_url, html)
        self.assertIn(last_image_url, html)

    def test__back_to_products_link_exists(self):
        response = self.client.get(reverse('product_details', kwargs={'slug': self.product.slug}))
        self.assertContains(response, reverse('products'))
