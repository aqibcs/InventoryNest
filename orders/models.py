from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from products.models import Product

class Order(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    READY_TO_SHIP = 'ready_to_ship'
    OUT_FOR_DELIVERY = 'out_for_delivery'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (READY_TO_SHIP, 'Ready to Ship'),
        (OUT_FOR_DELIVERY, 'Out for Delivery'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_display = self.user.username if self.user else self.guest_email
        return f"Order for {self.product.name} by {user_display}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.product.stock < self.quantity:
                raise ValueError("Not enough stock available.")
            self.product.stock -= self.quantity
            self.total_price = self.product.price * self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    def cancel(self):
        if self.status == self.PENDING:
            self.product.stock += self.quantity
            self.product.save()
            self.status = self.CANCELLED
            self.save()
        else:
            raise ValidationError("Order cannot be canceled once it is processed or shipped.")
