from rest_framework import serializers
from reviews.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
