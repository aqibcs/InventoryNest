from rest_framework import serializers
from .models import Product


class ProductsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'created_at',
            'updated_at', 'user'
        ]
