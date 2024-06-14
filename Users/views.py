from rest_framework import viewsets,permissions, status
from rest_framework.views import APIView
from rest_framework import generics,filters,pagination
from rest_framework.response import Response
from .models import CustomUser,Tutor,Wallet
from .serializers import (UserRegistrationSerializer,
                          UserSerializer,
                          CustomTokenObtainPairSerializer,
                          TutorInfoSerializer,
                          CombinedUserSerializer,
                          OtpValidationSerializer,
                          ChangePasswordSerializer,
                          WalletSerializer,
                          WalletHistorySerializer
                        )
from django.db.models import Q
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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
        if request.data['username']:
            username= request.data['username']
            print(username)
            if CustomUser.objects.filter(username=username).exists():
                return Response({'error':'username is already exists'},status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            user = serializer.save()    

            otp = generate_otp()
            user.otp =otp
            user.save()
            print(otp,'otp', user.email,'email')
            send_otp(user.email, otp)
        
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('hi serialiizer eroor is here')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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
            user.otp = 0
            if user.is_verified != True:
                user.is_verified = True
                user.save()
            else:
                pass
            return Response({'Detail':'otp verification successful'}, status=status.HTTP_201_CREATED)
        except:
            return Response ({'Detail':'Invalid OTP'}, status= status.HTTP_400_BAD_REQUEST)
    


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
    serializer_class = CombinedUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username' , 'first_name', 'last_name'] 

class FilterTutorView(generics.ListAPIView):
    print('this is filter tutor view')
    queryset = CustomUser.objects.filter(is_approved=True,is_tutor=True,is_verified=True,is_active=True)
    serializer_class = CombinedUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tutor__dialect'] 

class FilterTutorPreferenceView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_approved=True, is_tutor=True, is_verified=True, is_active=True)
    serializer_class = CombinedUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tutor__student_preferences']  # Ensure this field path is correct

    def get_queryset(self):
        queryset = super().get_queryset()
        student_preference = self.request.query_params.get('search', None)
        if student_preference:
            queryset = queryset.filter(tutor__student_preferences__contains=[student_preference])
        return queryset

# class GetTutors(APIView):
#     def get(self,request):
#         users=CustomUser.objects.filter(is_approved=True,is_tutor=True,is_verified=True,is_active=True,tutor__isnull=False)
#         for user in users:
            
class TutorRequestsViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_approved=False,is_verified=True,is_tutor=True,is_rejected=False,tutor__isnull=False)
    serializer_class = UserSerializer
    print(queryset)
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

@api_view(['GET'])
def users_count(request):

    try:
        total_users = CustomUser.objects.exclude(is_superuser=True).count()
        total_tutors = CustomUser.objects.filter(is_tutor=True,is_active=True).count()
        total_students = CustomUser.objects.filter(is_student=True,is_active=True).count()
        
        total_blocked_users = CustomUser.objects.filter(is_active=False).count()
        total_blocked_tutors = CustomUser.objects.filter(is_active=False,is_tutor=True).count()
        total_blocked_students = CustomUser.objects.filter(is_active=False,is_student=True).count()


        return Response({
            'total_users': total_users,
            'total_tutors': total_tutors,
            'total_students': total_students,
            'total_blocked_users': total_blocked_users,
            'total_blocked_tutors':total_blocked_tutors,
            'total_blocked_students': total_blocked_students
        }, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


class SearchUserTutorView(generics.ListAPIView):
    print('this is the search user view ')
    # queryset = CustomUser.objects.filter(is_superuser=False,is_active=True,is_verified=True,is_rejected=False)
    # print(queryset)
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username' , 'first_name', 'last_name'] 
    pagination_class = None
    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_superuser=False, is_active=True,is_verified=True)

        search_params = self.request.query_params.get('query')
        print(f'Search Parameters: {search_params}')  # Debugging search parameters
        return queryset

@api_view(['POST'])
def forgot_password_otp(request):
    
    if request.data.get('email'):
        email = request.data.get('email')
        print(email)
        user = CustomUser.objects.get(email=email)

        if user is not None:
            otp = generate_otp()
            user.otp =otp
            user.save()
            send_otp(user.email,otp)
            return Response({"success" :"otp send succesfully"}, status = status.HTTP_200_OK)

        else:
            return Response({"error" :"user is not found"}, status = status.HTTP_404_NOT_FOUND)

    else:
        return Response({"error":"sometthing went wrong"}, status = status.HTTP_400_BAD_REQUEST)
    

class WalletHistoryListView(generics.ListAPIView):
    serializer_class = WalletHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WalletHistory.objects.filter(user=user).order_by('-created_at')