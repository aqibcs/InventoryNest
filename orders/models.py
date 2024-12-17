from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from products.models import Product

class Order(models.Model):
    # Order Status Constants
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

    # Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders', null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_orders')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_display = self.user.username if self.user else self.guest_email
        return f"Order for {self.product.name} by {user_display}"

    def save(self, *args, **kwargs):
        if self._state.adding:  # New order
            if self.product.stock < self.quantity:
                raise ValidationError("Not enough stock available.")
            self.product.stock -= self.quantity
            self.product.save()

        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def cancel(self):
        """
        Cancel the order only if it's still pending.
        """
        if self.status != self.PENDING:
            raise ValidationError("Order cannot be canceled once it is processed or shipped.")
        self.product.stock += self.quantity
        self.product.save()
        self.status = self.CANCELLED
        self.save()

    @staticmethod
    def canceled_orders():
        """
        Retrieve all canceled orders.
        """
        return Order.objects.filter(status=Order.CANCELLED)

    @staticmethod
    def active_orders():
        """
        Retrieve orders that are not canceled or delivered.
        """
        return Order.objects.exclude(status__in=[Order.CANCELLED, Order.DELIVERED])
