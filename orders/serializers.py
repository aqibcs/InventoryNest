from rest_framework import serializers
from .models import Order
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.StringRelatedField(read_only=True)
    guest_email = serializers.EmailField(required=False, allow_blank=True)
    total_price = serializers.SerializerMethodField()  # Add total price field

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'guest_email', 'product', 'quantity', 'status',
            'created_at', 'updated_at', 'total_price'
        ]
        read_only_fields = ['created_at', 'updated_at']

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

    def validate(self, attrs):
        """
        Ensure that either a user or a guest email is provided.
        """
        user = self.context['request'].user
        guest_email = attrs.get('guest_email')

        if user.is_anonymous and not guest_email:
            raise serializers.ValidationError(
                {
                    "user": "You must be logged in or provide a guest email to place an order."
                }
            )
        return attrs

    def validate_status(self, value):
        """
        Ensure the status is valid and follows the progression logic.
        """
        valid_statuses = [
            'pending', 'processing', 'ready_to_ship', 'out_for_delivery',
            'delivered', 'cancelled'
        ]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"'{value}' is not a valid status. Choose from {valid_statuses}."
            )
        return value

    def get_total_price(self, obj):
        """
        Calculate the total price based on the product price and quantity.
        """
        return obj.product.price * obj.quantity

    def to_representation(self, instance):
        """
        Add additional product details in the serialized output.
        """
        representation = super().to_representation(instance)
        product = instance.product

        representation['product_details'] = {
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
        }
        return representation
