from rest_framework import generics, status
from authentication.serializers import *
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAuthenticated
from .permissions import *


# Create your views here.
class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPI(generics.CreateAPIView):
    serializer_class = UserDetailSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"error": "email or password is not correct"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            update_last_login(None, user)
            token, _ = Token.objects.get_or_create(user=user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


# 현진님의 코드 조금 수정함. 유저가 자신의 정보에만 접근할 수 있도록 permissions.py를 추가했음.
class SetUserInfoAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DoesUserMatchRequest]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class IdCheckAPI(generics.CreateAPIView):
    serializer_class = UserIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"email": "valid"}, status=status.HTTP_200_OK)


class LogoutAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print("token:", request.user.auth_token)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
