from rest_framework import serializers
from .models import Post
from .models import Comment
from django.conf import settings

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

    def validate(self, data):
        thumbnail = data.get("thumbnail", None)
        if thumbnail is not None:
            if thumbnail.name.lower().endswith('.png'):
                raise serializers.ValidationError("Invalid image file type: PNG files are not allowed.")
            return data
        return data
    
    def save(self):
        file = self.validated_data['thumbnail']
        if file:
            s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file.name}"
            self.validated_data['thumbnail'] = s3_url
        return super().save()

       

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"