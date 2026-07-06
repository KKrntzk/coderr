from django.conf import settings
from django.db import models


class Profile(models.Model):
    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        BUSINESS = "business", "Business"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    type = models.CharField(max_length=10, choices=UserType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.type})"
