# accounts/serializers.py
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User

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
    

    #모델을 request랑 response로 나누어서 관리하면 용이
    #request는 요청데이터의 serializer..