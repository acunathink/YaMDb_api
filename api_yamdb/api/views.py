from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail

from reviews.models import User
from .serializers import RegistrationSerializer
import secrets


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        # проверка корректности данных
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            # password = serializer.validated_data['password']
            code = secrets.token_hex(4).upper()

            # Создание пользователя
            user = User.objects.create_user(username=username, email=email)

            send_mail(
                subject='Another Beatles member',
                message=f'Вы сделали запрос на регистрацию на портале YaMDb.\n'
                        f'Ваш логин: {username}'
                        f'Для получения токена используйте код {code} и логин',
                from_email='robot@yamdb.pro',
                recipient_list=[email],
                fail_silently=True,
            )
            return Response({'message': f'Код потверждения был отправлен на указанный email.'})
        return Response(serializer.errors, status=400)


class TokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('last_name')

        # Проверка кода из запроса и логина пользователя
        if username and code:
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=400)

            # Проверка соответствия кода из запроса и кода пользователя
            if code == user.last_name:
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(token)

        return Response({'error': 'Неверные данные для получения токена'}, status=400)