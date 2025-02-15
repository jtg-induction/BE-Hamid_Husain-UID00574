from rest_framework import status
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from users.serializers import UserCreateSerializer, UserLoginSerializer


class UserRegistrationAPIView(mixins.CreateModelMixin, GenericAPIView):
    """
        success response format
         {
           first_name: "",
           last_name: "",
           email: "",
           date_joined: "",
           "token"
         }
    """
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()

        user.set_password(user.password)
        user.save()

        token = Token.objects.create(user=user)

        response_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_joined': user.date_joined,
            'token': token.key
        }
        return response_data


class UserLoginAPIView(GenericAPIView):
    """
        success response format
         {
           auth_token: ""
         }
    """
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)

        if user is None:
            return Response("Incorrect email or password", status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        return Response({"auth_token": token.key}, status=status.HTTP_200_OK)
