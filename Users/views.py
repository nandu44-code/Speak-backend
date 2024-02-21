from rest_framework import viewsets,permissions, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserRegistrationSerializer,UserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()  
    serializer_class = UserSerializer

class UserRegistrationViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.none() 
    serializer_class = UserRegistrationSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print("starting")
        token = super().get_token(user)

        # Add custom claims
        token["user"] = user.id
        token["is_tutor"] = user.is_tutor
        token["is_student"] = user.is_student
        token["is_superuser"] = user.is_superuser
        # ...
        print("ending")
        return token
class CustomTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = CustomTokenObtainPairSerializer