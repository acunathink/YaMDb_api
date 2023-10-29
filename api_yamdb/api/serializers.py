from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import User, Category, Genre, Title, Review, Comment


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


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для работы с Отзывами."""
    author = serializers.CharField(
        source='author.username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Serializer для работы с Категориями."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Serializer для работы с Жанрами."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    """Serializer для работы с Произведениями."""
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        category = get_object_or_404(Category, slug=data.get('category'))
        data['category'] = CategorySerializer(category).data

        genre_slugs = data.get('genre')
        genres = [get_object_or_404(Genre, slug=slug) for slug in genre_slugs]
        data['genre'] = GenreSerializer(genres, many=True).data

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
