from django.urls import path
from .views import logout, signup, login, get_profile, update_profile, delete_account

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('profile/', get_profile, name='get-profile'),
    path('profile/update/', update_profile, name='update-profile'),
    path('delete-account/', delete_account, name='delete-account'),
    path('logout/', logout, name='logout'),
]