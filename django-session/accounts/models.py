from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass 

    # 모델 내부 함수 구현 가능(이 모델에서만 접근가능하게 하려고, 안전)
    @staticmethod
    def get_user_or_none_by_username(username):

        try:
            return User.objects.get(username=username) # get()은 값이 없으면 에러를 띄우기 때문에 try-exception으로 처리
        except Exception:
            return None
        
    def get_user_or_none_by_email(email):

        try:
            return User.objects.get(email=email) 
        except Exception:
            return None