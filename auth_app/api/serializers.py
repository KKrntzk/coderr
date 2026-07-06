from django.contrib.auth.models import User
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
            "email": {"required": True, "allow_blank": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords do not match."}
            )

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "This email is already registered."}
            )

        return attrs

    def create(self, validated_data):
        user_type = validated_data.pop("type")
        validated_data.pop("repeated_password")
        password = validated_data.pop("password")

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        Profile.objects.create(user=user, type=user_type)

        return user
