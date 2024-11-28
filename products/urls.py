from django.urls import path
from .views import (create_product, list_products, get_product, update_product,
                    delete_product)

urlpatterns = [
    path('products/create/', create_product, name='product-create'),
    path('products/', list_products, name='product-list'),
    path('products/<int:pk>/', get_product, name='product-detail'),
    path('products/<int:pk>/update/', update_product, name='product-update'),
    path('products/<int:pk>/delete/', delete_product, name='product-delete'),
]
