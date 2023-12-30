from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import CustomTokenObtainPairView, OTPVerificationView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('otp/', OTPVerificationView.as_view(), name='token_otp'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
