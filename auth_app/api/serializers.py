from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from profile_app.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=Profile.UserType.choices, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Dieser Benutzername ist bereits vergeben.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Diese E-Mail-Adresse wird bereits verwendet.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Die Passwörter stimmen nicht überein."}
            )
        try:
            validate_password(attrs["password"])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs

    def create(self, validated_data):
        validated_data.pop("repeated_password")
        user_type = validated_data.pop("type")
        password = validated_data.pop("password")

        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(password)
        user.save()

        Profile.objects.create(user=user, type=user_type)
        return user
