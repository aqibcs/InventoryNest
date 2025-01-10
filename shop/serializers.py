from rest_framework import serializers
from .models import Shop

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'id', 'owner', 'shop_name', 'shop_description', 'shop_category',
            'business_address', 'phone_number', 'email', 'logo', 'cover_image',
            'shipping_policy', 'return_policy', 'facebook_link',
            'instagram_link', 'twitter_link', 'website_link', 'terms_accepted',
            'is_active', 'created_at', 'updated_at'
        ]

    def validate_terms_accepted(self, value):
        if not value:
            raise serializers.ValidationError("You must accept the terms and conditions to register the shop.")
        return value