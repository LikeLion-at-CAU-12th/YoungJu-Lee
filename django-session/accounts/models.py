from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    
    deleted_at = models.DateTimeField(null=True, blank=True)  
    # soft delete, db 데이터를 실제로 삭제하는 것이 아닌 삭제여부를 나타내는 속성을 통해 삭제를 표현

    request_at = models.DateTimeField(null=True, blank=True)
    # 회원 복구 요청 시간

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
        
    # 회원 탈퇴 함수
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()