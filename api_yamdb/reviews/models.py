from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
]


class BaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(
        max_length=254, unique=True,
        verbose_name='Электронная почта'
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        default='user', choices=ROLE_CHOICES,
        max_length=100, verbose_name='Роль'
    )
    confirmation_code = models.TextField(verbose_name='Код подтверждения')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(BaseModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveIntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    title = models.OneToOneField(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:25]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:25]
