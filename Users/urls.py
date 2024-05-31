from django.urls import (
    path,
    include
    )
from . import views
from .views import (
    UserViewSet,
    TutorViewSet,
    TutorRequestsViewSet,
    UserRegistrationViewSet,
    CustomTokenObtainPairView,
    TutorInfoViewSet,
    CustomUserTutorDetailView,
    TutorListView,
    SearchTutorView,
    SearchUserView,
    FilterTutorView,
    WalletViewSet,
    WalletByUserAPIView,
    users_count,
    )
    
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tutorlist',TutorViewSet)
router.register('requests',TutorRequestsViewSet)
# router.register('register', UserRegistrationViewSet, basename='register')
router.register('tutor/register', TutorInfoViewSet, basename='tutor/register')
# router.register('wallet', WalletViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<int:user_id>/', CustomUserTutorDetailView.as_view(), name='user-detail'),
    path('register/', UserRegistrationViewSet.as_view({'post': 'create'}), name='user-registration'),
    path('tutors/', TutorListView.as_view(), name='tutor_list'),
    path('validate-otp/', UserRegistrationViewSet.as_view({'post': 'validate_otp'}), name='validate-otp'),
    path('change-password/', UserViewSet.as_view({'post': 'change_password'}), name='user-change-password'),
    path('tutor-search/', SearchTutorView.as_view(), name='search-tutor'),
    path('tutor-filter/', FilterTutorView.as_view(), name='filter-tutor'),
    path('user-search/', SearchUserView.as_view(), name='search-user'),
    path('user-wallet/<int:user_id>/', WalletByUserAPIView.as_view(), name='wallet_by_user'),
    path('user-count/', users_count, name='user-count')
]