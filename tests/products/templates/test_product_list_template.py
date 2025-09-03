from django.test import TestCase
from django.urls import reverse
from lash_store.product.models import Product, ProductImages

class ProductListTemplateTests(TestCase):
    def setUp(self):
        self.products = []
        for i in range(3):
            product = Product.objects.create(
                name=f"Product {i}",
                slug=f"product-{i}",
                description="Описание",
                price=10.00 + i,
                stock=5
            )
            ProductImages.objects.create(product=product, image="products/img1.jpg")
            ProductImages.objects.create(product=product, image="products/img2.jpg")
            self.products.append(product)

    def test__template_renders_successfully(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_list.html')

    def test__products_are_displayed(self):
        response = self.client.get(reverse('products'))
        html_code = response.content.decode('utf-8')
        for product in self.products:
            self.assertContains(response, product.name)
            expected_price = f"Цена {product.price:.2f}".replace('.', ',') + " лв"
            self.assertIn(expected_price, html_code)

    def test__product_links_are_correct(self):
        response = self.client.get(reverse('products'))
        for product in self.products:
            detail_url = reverse('product_details', kwargs={'slug': product.slug})
            self.assertContains(response, detail_url)

    def test__images_are_displayed(self):
        response = self.client.get(reverse('products'))
        for product in self.products:
            first_image_url = product.images.first().image.url
            last_image_url = product.images.last().image.url
            self.assertContains(response, first_image_url)
            self.assertContains(response, last_image_url)

    def test__see_more_button_exists(self):
        response = self.client.get(reverse('products'))
        self.assertContains(response, "Повече информация")
