# urls.py
from django.urls import (
    path,
    include
    )
from .views import (
    UserViewSet,
    UserRegistrationViewSet,
    CustomTokenObtainPairView,
    TutorInfoViewSet,
    CustomUserTutorDetailView,
    TutorListView
    )
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )

router = DefaultRouter()
router.register('users', UserViewSet)
# router.register('register', UserRegistrationViewSet, basename='register')
router.register('tutor/register', TutorInfoViewSet, basename='tutor/register')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<int:user_id>/', CustomUserTutorDetailView.as_view(), name='user-detail'),
    path('register/', UserRegistrationViewSet.as_view({'post': 'create'}), name='user-registration'),
    path('tutors/', TutorListView.as_view(), name='tutor_list'),
    path('validate-otp/', UserRegistrationViewSet.as_view({'post': 'validate_otp'}), name='validate-otp'),
    path('change-password/', UserViewSet.as_view({'post': 'change_password'}), name='user-change-password')
          
]