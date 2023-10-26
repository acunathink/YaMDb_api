from rest_framework import serializers
from reviews.models import User


class RegistrationSerializer(serializers.Serializer):
    """Serializer для регистрации Пользователей."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')

    def validate_username(self, value):
        """Проверка использования допустимого username."""
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Serializer для работы с Токеном."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username',
                  'confirmation_code'
                  )


class UserSerializer(serializers.ModelSerializer):
    """Serializer для работы с Пользователями."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
