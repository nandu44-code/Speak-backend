# urls.py
from django.urls import path,include
from .views import UserViewSet, UserRegistrationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('register', UserRegistrationViewSet, basename='register')


urlpatterns = [
    path('', include(router.urls)),
]