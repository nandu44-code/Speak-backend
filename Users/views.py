from rest_framework import viewsets,permissions, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserRegistrationSerializer,UserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken

# views.py

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()  # Define queryset for UserViewSet
    serializer_class = UserSerializer

class UserRegistrationViewSet(viewsets.ModelViewSet):
    # print("hellow there")
    queryset = CustomUser.objects.none() 
    serializer_class = UserRegistrationSerializer

# class UserLoginViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     def create(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data.get('email')
#         password = serializer.validated_data.get('password')

#         # Authenticate user
#         user = authenticate(email=email, password=password)

#         if user:
#             # Generate JWT tokens
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'email': CustomUser.email,
#                 'access_token': str(refresh.access_token),
#                 'refresh_token': str(refresh)
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid username or password'},status=status.HTTP_400_BAD_REQUEST)
