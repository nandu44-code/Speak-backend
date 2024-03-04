from rest_framework import viewsets,permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser,Tutor
from .serializers import (UserRegistrationSerializer,
                        UserSerializer,
                        TutorInfoSerializer,
                        CombinedUserSerializer,
                        OtpValidationSerializer)

from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .utils import generate_otp
from .tasks import send_otp

@permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()  
    serializer_class = UserSerializer


class UserRegistrationViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.none() 
    serializer_class = UserRegistrationSerializer

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            otp = generate_otp()
            print(otp,"otp from create function")
            user.otp=otp
            user.save()
        except exception as e:
            print(e)

        send_otp(user.email, otp)
        request.session['useremail'] = user.email

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def validate_otp(self,request,*args,**kwargs):
        print("starting validate otp")
        serializer = OtpValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('serializer is okay')
        otp_to_check = serializer.validated_data.get('otp')
        email_to_check = request.session.get('useremail')
        
        if email_to_check is None:
            # return Response({'Detail': 'Invalid session or no useremail found'}, status=status.HTTP_400_BAD_REQUEST)
            print('no session')
       
        print(otp_to_check, 'otp')
        print(email_to_check, 'email')
        try:
            user = CustomUser.objects.get(email = email_to_check, otp = otp_to_check)
            user.otp = None
            user.is_verified = True
            user.save()

            return Response({'Detail':'otp verification successful'}, status=status.HTTP_201_CREATED)
        except:

            return Response ({'Detail':'Invalid OTP'}, status= status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.is_verified:

            token = super().get_token(user)

            token["user"] = user.id
            token["is_tutor"] = user.is_tutor
            token["is_student"] = user.is_student
            token["is_superuser"] = user.is_superuser

            return token
        else:
            raise Exception('User is not verified')

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