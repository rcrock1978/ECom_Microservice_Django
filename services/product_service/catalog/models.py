# Expose models at the package level so Django can discover them
from .infrastructure.models import Category, Product

__all__ = ['Category', 'Product']
