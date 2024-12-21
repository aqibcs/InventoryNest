from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'product_details', 'total_price']
    
    def get_product_details(self, obj):
        product = obj.product
        return {
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        }
    
    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

    def validate_quantity(self, value):
        """
        Ensure that the ordered quantity does not exceed available stock.
        """
        product_id = self.initial_data.get('product')
        try:
            product_instance = Product.objects.get(id=product_id)
            if value > product_instance.stock:
                raise serializers.ValidationError(
                    f"Only {product_instance.stock} items are available in stock."
                )
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product not found.')
        return value



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'created_at', 'items']
    
    def create(self, validated_data):
        """
        Create a cart if it doesn't exist for the user or session.
        """
        user = validated_data.get('user')
        session_id = validated_data.get('session_id')
        cart, created, = Cart.objects.get_or_create(user=user, session_id=session_id)
        return cart