from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from communication.models import WebSocketConsumerAccessesModel

from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
JWT_authenticator = JWTAuthentication()


class AccessesRequestView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        def p401():
            _ = HttpResponse("null")
            _.status_code = status.HTTP_401_UNAUTHORIZED
            return _

        try:
            response = JWT_authenticator.authenticate(request)
            if response is not None:
                # unpacking
                user, token = response
                accesses = WebSocketConsumerAccessesModel.objects.create(user=user)
                return Response({'accesses': accesses.accesses_token}, 201)
        except Exception as e:
            print(e)
        return p401()
