from django.urls import path

from .api.views import RegistrationView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
]
