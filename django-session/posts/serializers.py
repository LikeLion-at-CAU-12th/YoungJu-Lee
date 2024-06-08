from rest_framework import serializers
from .models import Post
from .models import Comment

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

    def validate(self, data):
        thumbnail = data.get("thumbnail", None)
        if thumbnail is not None:
            if thumbnail.name.lower().endswith('.png'):
                raise serializers.ValidationError("Invalid image file type: PNG files are not allowed.")


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"