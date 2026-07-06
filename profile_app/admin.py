from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "created_at")
    list_filter = ("type",)
    search_fields = ("user__username",)
