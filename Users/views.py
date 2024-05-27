from rest_framework import viewsets,permissions, status
from rest_framework.views import APIView
from rest_framework import generics,filters,pagination
from rest_framework.response import Response
from .models import CustomUser,Tutor,Wallet
from .serializers import (UserRegistrationSerializer,
                          UserSerializer,
                          TutorInfoSerializer,
                          CombinedUserSerializer,
                          OtpValidationSerializer,
                          ChangePasswordSerializer,
                          WalletSerializer
                        )
from django.db.models import Q
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,action
from .utils import generate_otp,send_otp
# from .tasks import send_otp_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view

# @permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_student=True)  
    serializer_class = UserSerializer
    pagination_class = pagination.PageNumberPagination

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            password = serializer.data.get('password')
         
            user.set_password(password)
            user.save()

            return Response({'message': 'Password changed successfully'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TutorViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_tutor=True)
    serializer_class = UserSerializer

class SearchUserView(generics.ListAPIView):
    print('this is the search user view ')
    queryset = CustomUser.objects.filter(is_student=True)
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username' , 'first_name', 'last_name'] 


class UserRegistrationViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.none() 
    serializer_class = UserRegistrationSerializer

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()    

        otp = generate_otp()
        user.otp =otp
        user.save()
        print(otp,'otp', user.email,'email')
        send_otp(user.email, otp)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    

    def validate_otp(self,request,*args,**kwargs):
        print("starting validate otp")
        serializer = OtpValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('serializer is okay')
        
        otp_to_check = serializer.validated_data.get('otp')
        # email_to_check = request.session.get('useremail')
        
        # if email_to_check is None:
        #     # return Response({'Detail': 'Invalid session or no useremail found'}, status=status.HTTP_400_BAD_REQUEST)
        #     print('no session')
       
        print(otp_to_check, 'otp')
        # print(email_to_check, 'email')
        print("before try")
        try:
            print('in the try')
            print(type(otp_to_check))
            user = CustomUser.objects.get( otp = otp_to_check)
            print(user.otp)
            print('1')
            user.otp = 0
            print('2')

            user.is_verified = True
            print('3')
            user.save()
            print('4')

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
            token["is_approved"] = user.is_approved
            token["is_rejected"] = user.is_rejected
            if user.is_tutor:
                try:
                    tutor = Tutor.objects.get(user=user)
                    token["tutor"] = tutor.id
                except:
                    pass 
            return token
        else:
            raise Exception('User is not verified')

class CustomTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = CustomTokenObtainPairSerializer

class TutorInfoViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorInfoSerializer
    # pagination_class = pagination.PageNumberPagination


class CustomUserTutorDetailView(APIView):
    def get(self, request, user_id):
        try:
            custom_user = CustomUser.objects.select_related('tutor').get(id=user_id)
            serializer = CombinedUserSerializer(custom_user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=404)

class TutorListView(APIView):
    def get(self, request):
        users = CustomUser.objects.filter(is_approved=True,is_tutor=True,is_verified=True,is_active=True)
        serializer = CombinedUserSerializer(users, many=True)
        return Response(serializer.data)

class SearchTutorView(generics.ListAPIView):
    print('this is seratch tutor view')
    queryset = CustomUser.objects.filter(is_approved=True,is_tutor=True,is_verified=True,is_active=True)
    print(queryset)
    serializer_class = CombinedUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username' , 'first_name', 'last_name'] 

class FilterTutorView(generics.ListAPIView):
    print('this is filter tutor view')
    queryset = CustomUser.objects.filter(is_approved=True,is_tutor=True,is_verified=True,is_active=True)
    print(queryset)
    serializer_class = CombinedUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['dialect'] 

# class GetTutors(APIView):
#     def get(self,request):
#         users=CustomUser.objects.filter(is_approved=True,is_tutor=True,is_verified=True,is_active=True,tutor__isnull=False)
#         for user in users:
            
class TutorRequestsViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_approved=False,is_verified=True,is_tutor=True,is_rejected=False,tutor__isnull=False)
    serializer_class = UserSerializer
    
    def get_queryset(self):

        return CustomUser.objects.filter(is_approved=False,is_verified=True,is_tutor=True,is_rejected=False,tutor__isnull=False).distinct()

class WalletViewSet(viewsets.ModelViewSet):
    queryset= Wallet.objects.all()
    serializer_class = WalletSerializer

class WalletByUserAPIView(APIView):
    def get(self, request, user_id):
        try:
            print(user_id)
            wallet = Wallet.objects.get(user=user_id)
            serializer = WalletSerializer(wallet)
            print(wallet)
            print('hi')
            print(serializer.data)
            return Response(serializer.data)
        except Wallet.DoesNotExist:
            return Response({"message": "Wallet not found for the given user ID"}, status=status.HTTP_404_NOT_FOUND)