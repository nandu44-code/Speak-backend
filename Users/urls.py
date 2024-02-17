# urls.py
from django.urls import path,include
from .views import UserViewSet, UserRegistrationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('register', UserRegistrationViewSet, basename='register')
# router.register(r'user-login', UserLoginViewSet, basename='user-login')

urlpatterns = [
    path('', include(router.urls)),
]