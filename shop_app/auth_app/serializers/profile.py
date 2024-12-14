from auth_app.models.profile import Profile
from auth_app.serializers.avatar import OutAvatarSerializer
from auth_app.utils import PhoneValidator
from django.core.validators import EmailValidator
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer[Profile]):
    """
    Класс-сериализатор для профиля пользователя.
    """

    fullName = serializers.CharField(
        source="full_name", min_length=2, max_length=150, required=True
    )
    email = serializers.CharField(required=True, validators=[EmailValidator()])
    phone = serializers.CharField(required=True, validators=[PhoneValidator()])
    avatar = OutAvatarSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]
