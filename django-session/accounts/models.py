from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass #해당 세션에서 바로 유저모델을 사용할 것은 아니기 때문에 pass로 넣겠습니다.