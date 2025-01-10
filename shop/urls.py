from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.create_shop, name='create_shop'),  # Create shop
    path('shop/profile/', views.get_shop, name='get_shop'),  # Get shop profile
    path('shop/update/', views.update_shop, name='update_shop'),  # Update shop profile
    path('shop/delete/', views.delete_shop, name='delete_shop'),  # Delete shop profile
]
