# urls.py
from django.urls import (
    path,
    include
    )
from .views import (
    UserViewSet,
    UserRegistrationViewSet,
    CustomTokenObtainPairView
    )
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('register', UserRegistrationViewSet, basename='register')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]