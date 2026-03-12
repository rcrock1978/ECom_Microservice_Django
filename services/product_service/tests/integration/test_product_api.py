import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.product_service.product_service.settings')
import django
from django.test import TestCase

# ensure settings are loaded before importing anything else
django.setup()


class ProductApiTests(TestCase):
    def test_list_products_empty(self):
        resp = self.client.get("/products/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_category_tree(self):
        resp = self.client.get("/categories/")
        assert resp.status_code == 200

    def test_internal_product_lookup(self):
        resp = self.client.get("/internal/products/1/")
        assert resp.status_code in (200, 404)
