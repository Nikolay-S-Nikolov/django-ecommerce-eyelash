class DetailProductViewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            description="Test description",
            price=20.00,
            stock=10
        )

    def test_detail_view_status_code(self):
        response = self.client.get(reverse('product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_context(self):
        response = self.client.get(reverse('product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.context['object'], self.product)

    def test_detail_view_404(self):
        response = self.client.get(reverse('product_detail', kwargs={'slug': 'non-existent'}))
        self.assertEqual(response.status_code, 404)
