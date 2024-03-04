from rest_framework import viewsets,permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser,Tutor
from .serializers import UserRegistrationSerializer,UserSerializer,TutorInfoSerializer,CombinedUserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()  
    serializer_class = UserSerializer


class UserRegistrationViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.none() 
    serializer_class = UserRegistrationSerializer

   

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token["user"] = user.id
        token["is_tutor"] = user.is_tutor
        token["is_student"] = user.is_student
        token["is_superuser"] = user.is_superuser

        return token
class CustomTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = CustomTokenObtainPairSerializer

class TutorInfoViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorInfoSerializer

class CustomUserTutorDetailView(APIView):
    def get(self, request, user_id):
        try:
            custom_user = CustomUser.objects.select_related('tutor').get(id=user_id)
            serializer = CombinedUserSerializer(custom_user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=404)