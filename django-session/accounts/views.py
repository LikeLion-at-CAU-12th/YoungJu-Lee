from django.shortcuts import render
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404 
from accounts.serializers import RegisterSerializer
from accounts.serializers import AuthSerializer
from accounts.serializers import RestoreSerializer
from accounts.serializers import OAuthSerializer
from accounts.models import User

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
    

class DeleteView(APIView):
    # 회원 탈퇴
   permission_classes = [IsAuthenticated]

   def delete(self, request):
        user = request.user
        user.soft_delete()
        res = Response(
                {
                    "user" :{
                        "id" : user.id,
                        "email" : user.email,
                        "deleted_at" : user.deleted_at
                    },
                    "message" : "회원 탈퇴 성공",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return res

class RestoreView(APIView):
    # 회원 복구
    def post(self, request):
        username = request.data.get('username')
        user = User.get_user_or_none_by_username(username)
        serializer = RestoreSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            res = Response(
                {
                    "user" :{
                        "id" : user.id,
                        "email" : user.email,
                        "deleted_at" : user.deleted_at
                    },
                    "message" : "회원 복구 성공",
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        else:
            return Response({"message":"회원 복구 실패"}, status=status.HTTP_400_BAD_REQUEST)

            
from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, "secrets.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

GOOGLE_SCOPE_USERINFO = get_secret("GOOGLE_SCOPE_USERINFO")
GOOGLE_REDIRECT = get_secret("GOOGLE_REDIRECT")
GOOGLE_CALLBACK_URI = get_secret("GOOGLE_CALLBACK_URI")
GOOGLE_CLIENT_ID = get_secret("GOOGLE_CLIENT_ID")
GOOGLE_SECRET = get_secret("GOOGLE_SECRET")

from django.shortcuts import redirect
from json import JSONDecodeError
from django.http import JsonResponse
import requests
from allauth.socialaccount.models import SocialAccount


# 구글 로그인 페이지로 넘어간다
def google_login(request):
   scope = GOOGLE_SCOPE_USERINFO        # + "https://www.googleapis.com/auth/drive.readonly" 등 scope 설정 후 자율적으로 추가
   return redirect(f"{GOOGLE_REDIRECT}?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

# 인가 코드를 받고 그것을 이용해 access token을 발급받는다
def google_callback(request):
    code = request.GET.get("code")      # Query String 으로 넘어옴
    
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)

    google_access_token = token_req_json.get('access_token')
    # access toke으로 구글 계정 이메일 정보를 가져온다
    email_response = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={google_access_token}")
    res_status = email_response.status_code

    if res_status != 200:
        return JsonResponse({'status': 400,'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    
    email_res_json = email_response.json()
    # email = email_res_json.get('email')

    # 이메일이 존재하면 계정정보를 가져온다
    serializer = OAuthSerializer(data=email_res_json)
    try:
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]

            social_user = SocialAccount.objects.get(user=user)

            if social_user is None:
                return JsonResponse({"message":"Not existing google account user"}, status=status.HTTP_404_NOT_FOUND)
            
            if social_user.provider != 'google':
                return JsonResponse({"message":"Not a google account."}, status=status.HTTP_400_BAD_REQUEST)
            
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            res = JsonResponse(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
    except:       # 회원가입이 필요함
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


KAKAO_REDIRECT = get_secret('KAKAO_REDIRECT_URI')
KAKAO_CLIENT_ID = get_secret('KAKAO_REST_API_KEY')
KAKAO_CLIENT_SECRET_KEY = get_secret('KAKAO_CLIENT_SECRET_KEY')

kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

def kakao_login(request):
    return redirect(f"{kakao_login_uri}?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT}&response_type=code")

def kakao_callback(request):
    code = request.GET.get("code")      # Query String 으로 넘어옴
    
    if code is None:
        return JsonResponse({"error":"code error"},status=status.HTTP_400_BAD_REQUEST)

    request_data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_CLIENT_ID,
        'redirect_uri': KAKAO_REDIRECT,
        'client_secret': KAKAO_CLIENT_SECRET_KEY,
        'code': code,
    }
    token_headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }

    token_req = requests.post(kakao_token_uri, data=request_data, headers=token_headers)
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)

    print(token_req_json)
    kakao_access_token = token_req_json.get('access_token')

    if kakao_access_token is None:
        return JsonResponse({"error":"access token error"},status=status.HTTP_400_BAD_REQUEST)

    # access token으로 카카오 계정 정보를 요청한다

    kakao_access_token = f"Bearer {kakao_access_token}"
    auth_headers = {
        "Authorization": kakao_access_token,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    kakao_user_info = requests.get(kakao_profile_uri, headers=auth_headers)
    print(kakao_user_info)

    res_status = kakao_user_info.status_code
    if res_status != 200:
        return JsonResponse({'message': 'You failed to get user info'}, status=status.HTTP_400_BAD_REQUEST)
    
    kakao_user_info_json = kakao_user_info.json()
   
    # 이메일이 존재하면 계정정보를 가져온다
    serializer =  OAuthSerializer(data=kakao_user_info_json)
    try:
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]

            # social_user = SocialAccount.objects.get(user=user)

            # if social_user is None:
            #     return JsonResponse({"message":"Not existing google account user"}, status=status.HTTP_404_NOT_FOUND)
            
            # if social_user.provider != 'google':
            #     return JsonResponse({"message":"Not a google account."}, status=status.HTTP_400_BAD_REQUEST)
            
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            res = JsonResponse(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
    except:       # 회원가입이 필요함
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
