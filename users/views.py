from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({'user': UserSerializer(user).data,
                         'access': str(refresh.access_token),
                         'refresh': str(refresh)}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({'user': UserSerializer(user).data,
                         'access': str(refresh.access_token),
                         'refresh': str(refresh)})