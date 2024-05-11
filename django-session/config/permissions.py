from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied,NotAuthenticated

# header에 나만의 비밀스러운 key 값을 입력받은 후 key 문구에 맞게 입력한 사용자만 모든 API 요청 허용
class SecretKey(BasePermission):
    def has_permission(self, request, view):
        secret_key = "likelion"
        try:
            input_key = request.headers.get('key')
            if input_key == secret_key:
                return True
            else:
                raise PermissionDenied("Incorrect Secret Key")
        except Exception:
            raise PermissionDenied("Incorrect Secret Key")
            

# 게시글 작성자만 수정, 삭제 가능. 이외는 읽기 권한만

class IsWriterOrReadOnly(SecretKey):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated:  # 타고 타고 가서 속성 확인가능
                if request.user == obj.user_id:
                    return True
                raise PermissionDenied("No permission to this object")
            raise NotAuthenticated("Not Authenticated")
