from django.db import models
from django.contrib.auth.models import User


class Shop(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')

    shop_name = models.CharField(max_length=255, unique=True)
    shop_description = models.TextField()
    shop_category = models.CharField(max_length=255)
    business_address = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255)
    logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='shop_covers/', blank=True, null=True)

    # Shipping and Delivery Information
    shipping_policy = models.TextField(blank=True, null=True)
    return_policy = models.TextField(blank=True, null=True)

    # Social Media and External Links
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)

    # Terms and Conditions agreement
    terms_accepted = models.BooleanField(default=False)

    # Shop Status (whether it is active or not)
    is_active = models.BooleanField(default=False)

    # Date when the shop was created
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name