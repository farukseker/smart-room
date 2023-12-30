import pyotp
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as rest_status
from Auth.models import OTPDevice


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class OTPVerificationView(APIView):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        otp_code = request.data.get('otp_code')
        if user.is_authenticated and OTPDevice.otp_verify(user, otp_code):
            return Response(status=rest_status.HTTP_200_OK)
        return Response({}, status=rest_status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

