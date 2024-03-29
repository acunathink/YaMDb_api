from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title, User

from .permissions import (
    AuthorOrModerPermission, IsAdminOrReadOnlyPermission, IsAdminPermission
)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    RegistrationSerializer, ReviewSerializer, TitlesSerializer,
    TokenSerializer, UserSerializer
)


class CategoriesGenresBaseMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Миксин для Жанров и Категорий.

    Разрешает получение списка, создание объекта,
    удаление объекта."""
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class RegistrationView(APIView):
    """Регистрация пользователя и отправка confirmation_code на email."""
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        existing_user = User.objects.filter(username=username).first()

        if existing_user and existing_user.email != email:
            return Response(
                f'Указан не верный email для {existing_user}!',
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            return Response(
                request.data,
                status=status.HTTP_200_OK
            )
        if existing_user is None and User.objects.filter(email=email).exists():
            return Response(
                f'Пользователь с почтой {email} уже зарегистрирован!',
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                request.data,
                status=status.HTTP_200_OK
            )
        user = User.objects.create_user(username, email)
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()

        send_mail(
            subject='Confirmation code for token',
            message=f'Вы сделали запрос на регистрацию на портале YaMDb.\n\n'
                    f'Ваш логин: {user.username} \n'
                    f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    """Получение токена по username и confirmation_code."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                'Указан не корректный "confirmation_code"',
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Работа с полями Пользователей."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdminPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        url_path='me',
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_about_me(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if self.request.method == 'PATCH':
            serializer.validated_data.pop('role', None)
            serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CategoriesViewSet(CategoriesGenresBaseMixin):
    """Работа с Категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)


class GenresViewSet(CategoriesGenresBaseMixin):
    """Работа с Жанрами."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)


class TitlesViewSet(viewsets.ModelViewSet):
    """Работа с Произведениями."""
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnlyPermission,)

    def update(self, request, *args, **kwargs):
        if self.action == 'update':
            return Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class WithTitleViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrModerPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title


class ReviewsViewSet(WithTitleViewSet):
    """Работа с Отзывами."""
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(WithTitleViewSet):
    """Работа с Комментариями."""
    serializer_class = CommentSerializer

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review(),
            title=self.get_title()
        )
