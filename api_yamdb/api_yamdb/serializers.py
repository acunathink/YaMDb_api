from rest_framework import serializers
from reviews.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = '__all__'


class JWTTokenSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'
