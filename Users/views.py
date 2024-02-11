from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserRegistrationSerializer,UserSerializer

# views.py

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()  # Define queryset for UserViewSet
    serializer_class = UserSerializer

class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.none()  # This is just a placeholder queryset since we are not using a queryset for registration
    serializer_class = UserRegistrationSerializer
