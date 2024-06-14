from .models import CustomUser,Tutor,Wallet,WalletHistory
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
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
        print('updatinggg')
        password = validated_data.get('password')   
        if 'password' in validated_data:

            print('password is in validated data')
            instance.set_password(validated_data['password'])
      
        return super().update(instance, validated_data)

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

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            print('username already exists')
            raise serializers.ValidationError('username Already exists')
        return value

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user = CustomUser.objects.create_user(**validated_data)
        user.groups.set(groups)  # Use set() to assign groups
        return user

class   TutorInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tutor
        fields = '__all__'

class CombinedUserSerializer(serializers.ModelSerializer):
    tutor = TutorInfoSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_image', 'last_name', 'first_name', 'is_active', 'tutor']


class OtpValidationSerializer(serializers.Serializer):
    otp = serializers.IntegerField()

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required = True)
    

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model= Wallet
        fields = '__all__'

class WalletHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletHistory
        fields = ['id', 'wallet', 'user', 'amount', 'created_at']