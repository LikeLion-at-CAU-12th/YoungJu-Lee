from django.shortcuts import render
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import RegisterSerializer
from accounts.serializers import AuthSerializer

# Create your views here.

class RegisterView(APIView):
    # 회원가입 메소드
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True): # serializer 내 validate 함수 실행
            user = serializer.save(request) # serializer 내 save 함수 실행
            token = RefreshToken.for_user(user)
            refresh_token =str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user" : serializer.data,
                    "message" : "register success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status = status.HTTP_201_CREATED,
            )
            return res 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AuthView(APIView):
    # 인증 메소드
    def post(self, request):
        serializer = AuthSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            access_token = serializer.validated_data['access_token']
            refresh_token = serializer.validated_data['refresh_token']
            res = Response(
                {
                    "user" :{
                        "id" : user.id,
                        "email" : user.email,
                    },
                    "message" : "login success",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated

class LogoutView(APIView):
    # 로그아웃 메소드
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({"messge": "로그아웃되었습니다."}, status=status.HTTP_200_OK)