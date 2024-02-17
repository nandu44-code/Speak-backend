from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         user = authenticate(email=email, password=password)

#         if not user:
#             raise serializers.ValidationError("Invalid username or password")

#         refresh = RefreshToken.for_user(user)

#         return {
#             'username': CustomUser.email,
#             'access_token': str(refresh.access_token),
#             'refresh_token': str(refresh)
#         }