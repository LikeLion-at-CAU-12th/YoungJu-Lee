# accounts/serializers.py
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

# 회원가입
class RegisterSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(required=True) # 필수 input이라는 뜻
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['password', 'username', 'email'] # 위에 썼으면 얘도 필수

    # 사용자(user) 생성 코드    
    def save(self, request):

        user = User.objects.create(
            username=self.validated_data['username'],  # validated_data는 serializer.is_valid()로 유효성 검증 통과한 값들
            email=self.validated_data['email'],
        )

        # password는 암호화해서 저장
        user.set_password(self.validated_data['password']) # set_password()로 암호화해서 DB에 저장
        user.save()

        return user
    
    # 유효성 검사 코드
    def validate(self, data):
        email = data.get('email', None)  # 없으면 None 반환

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('email already exists')
        
        return data
    
# 인증
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']
    
    def validate(self,data):

        username = data.get("username", None)
        password = data.get("password", None)

        user = User.get_user_or_none_by_username(username=username) # model 함수

        if user.deleted_at is not None:
            raise serializers.ValidationError("이미 탈퇴한 회원입니다.")
        
        if user is None: 
            raise serializers.ValidationError("user account not exist")
        else:
            if not user.check_password(raw_password=password):
                raise serializers.ValidationError("wrong password")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data

class RestoreSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']
        
    def validate(self, data):
        # 아이디, 비밀번호를 맞게 입력한 경우 복구한다.
        username = data.get("username", None)
        password = data.get("password", None)

        user = User.get_user_or_none_by_username(username=username)

        if user is None: 
            raise serializers.ValidationError("존재하지 않는 회원입니다.")
        if user.deleted_at is None:
            raise serializers.ValidationError("존재하는 회원입니다.")
        if not user.check_password(password):
            raise serializers.ValidationError("잘못된 비밀번호 입니다.")

        return data

    def save(self):
        user = self.instance
        user.request_at = timezone.now()
        user.deleted_at = None
        user.save()
        
        return user

from allauth.socialaccount.models import SocialAccount

class OAuthSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, data):
        email = data.get("email", None)
        
        user = User.get_user_or_none_by_email(email=email)

        if user is None:
            raise serializers.ValidationError("Not existing user account")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data

