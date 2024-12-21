from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify-email/<uid>/<token>/', views.verify_email, name='verify_email'),
    path('login/', views.login, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('profile/', views.view_profile, name='manage_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('logout/', views.logout, name='logout'),
]
