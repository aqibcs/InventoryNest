from rest_framework import serializers
from .models import Order
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.StringRelatedField(read_only=True)
    guest_email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'guest_email', 'product', 'quantity', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']

    def validate_quantity(self, value):
        """
        Ensure that the ordered quantity does not exceed available stock.
        """
        product_id = self.initial_data.get('product')
        try:
            product_instance = Product.objects.get(id=product_id)
            if value > product_instance.stock:
                raise serializers.ValidationError('Not enough stock available.')
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product not found.')
        return value

    def validate(self, attrs):
        """
        Ensure that either a user or a guest email is provided.
        """
        user = self.context['request'].user
        guest_email = attrs.get('guest_email')

        if user.is_anonymous and not guest_email:
            raise serializers.ValidationError(
                "Either an authenticated user or a guest email is required."
            )
        return attrs