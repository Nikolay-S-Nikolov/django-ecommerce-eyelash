from django.test import TestCase
from django.urls import reverse
from lash_store.product.models import Product

class DetailProductViewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test description",
            price=20.00,
            stock=10
        )

    def test__detail_view_status_code_200(self):
        response = self.client.get(reverse('product_details', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)

    def test__detail_view_correct_context(self):
        response = self.client.get(reverse('product_details', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.context['object'], self.product)

    def test__detail_view_404(self):
        response = self.client.get(reverse('product_details', kwargs={'slug': 'non-existent'}))
        self.assertEqual(response.status_code, 404)
