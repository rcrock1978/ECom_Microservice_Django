from rest_framework.views import APIView
from rest_framework.response import Response

from services.product_service.catalog.infrastructure.repositories import ProductRepository, CategoryRepository
from services.product_service.catalog.infrastructure.models import Product
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategoryTreeSerializer,
)


class ProductListView(APIView):
    def get(self, request):
        keyword = request.query_params.get('q')
        category_id = request.query_params.get('category')
        products = ProductRepository().list(keyword=keyword, category_id=category_id)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    def get(self, request, slug):
        product = ProductRepository().get_by_slug(slug)
        if not product:
            return Response(status=404)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class CategoryListView(APIView):
    def get(self, request):
        cats = CategoryRepository().list_roots()
        serializer = CategoryTreeSerializer(cats, many=True)
        return Response(serializer.data)


class InternalProductView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=404)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)
