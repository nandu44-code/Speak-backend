from .models import CustomUser,Tutor
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

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

class CombinedUserSerializer(serializers.ModelSerializer):
    tutor = TutorInfoSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_image', 'tutor']


class OtpValidationSerializer(serializers.Serializer):
    otp = serializers.IntegerField()



class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required = True)
    
