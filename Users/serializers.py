from .models import CustomUser,Tutor
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
    def partial_update(self, instance, validated_data):
      
        return super().update(instance, validated_data)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class TutorInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tutor
        fields = '__all__'


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Add custom claims to the token, if needed
#         token['username'] = user.username
#         token['is_superuser'] = user.is_superuser
#         token['is_tutor'] = user.is_tutor
#         token['is_student'] = user.is_student
#         return token

# class CustomTokenRefreshSerializer(TokenRefreshSerializer):
#     pass