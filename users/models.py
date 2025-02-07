from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    address = models.TextField(blank=True, null=True)
    payment_info = models.JSONField(blank=True, null=True)
    preferences = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
