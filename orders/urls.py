from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('orders/create/', views.process_order, name='create_order'),  # Create order (public access)

    # Authenticated URLs
    path('orders/', views.list_orders, name='list_orders'),  # List all orders (GET)
    path('orders/<int:order_id>/', views.get_order, name='get_order'),  # Retrieve a specific order (GET)
    path('orders/<int:order_id>/update/', views.update_order, name='update_order'),  # Update order (PUT/PATCH)
    path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),  # Delete order (DELETE)
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),  # Cancel order (POST)
]
