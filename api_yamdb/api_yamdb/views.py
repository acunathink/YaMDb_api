from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail

from reviews.models import User
from .serializers import UserRegistrationSerializer
import secrets


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        # проверка корректности данных
        if serializer.is_valid():
            username = serializer.validated_data['username']
            # email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            code = secrets.token_hex(4)

            # Создание пользователя
            # user = User.objects.create_user(username=username, email=email, password=password)
            user = User.objects.create_user(username=username, password=password)
            return Response({'message': f'Код {code} для пользователя {username} отправлен на указанный email'})
        return Response(serializer.errors, status=400)