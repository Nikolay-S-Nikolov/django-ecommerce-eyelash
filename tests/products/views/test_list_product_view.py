from django.test import TestCase
from django.urls import reverse
from lash_store.product.models import Product

class ListProductViewTests(TestCase):
    def setUp(self):
        for i in range(10):
            Product.objects.create(
                name=f"Product {i}",
                description="Test description",
                price=10.00,
                stock=5
            )

    def test__list_view_status_code_200(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)

    def test__list_view_correct_pagination(self):
        response = self.client.get(reverse('products'))
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['object_list']), 6)

    def test__list_view_correct_ordering(self):
        response = self.client.get(reverse('products'))
        products = response.context['object_list']
        dates = [product.created_at for product in products]
        self.assertEqual(dates, sorted(dates, reverse=True))
