from django.db import models
from accounts.models import User

## 추상 클래스 정의
class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract = True

class Post(BaseModel):

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="제목", max_length=20)
    content = models.TextField(verbose_name="내용")
    user_id = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, db_column="user_id")
    category = models.CharField(choices=CHOICES, max_length=20)

class Comment(BaseModel):
    id = models.IntegerField(primary_key=True)
    comments = models.TextField(verbose_name="코멘트")
<<<<<<< HEAD
    post_id = models.ForeignKey("Post", related_name="post", on_delete=models.CASCADE, db_column="post_id")
    user_id = models.CharField(verbose_name="유저 아이디", max_length=10)
    is_secret = models.BooleanField(verbose_name="비밀댓글", default=False)
=======
    post_id = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, db_column="post_id")
    user_id = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE, db_column="user_id")
    is_secret = models.BooleanField(verbose_name="비밀댓글", default=False)
    

   
# class Post_HashTag(models.Model):  # 중간 테이블 직접 작성할 경우
#     post_id = models.ForeignKey("Post", on_delete=models.CASCADE, db_column="post_id")
#     hashtag_id = models.ForeignKey("HashTag", on_delete=models.CASCADE, db_column="hashtag_id")
>>>>>>> 68df8f3 (fix : user_id 속성 자료형 수정)
