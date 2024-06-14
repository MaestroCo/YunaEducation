from rest_framework import serializers
from .models import Course, Lesson, Comment, Notification, LikeLesson, DislikeLesson
from django.contrib.auth.models import User
from .utils import validate_password


# Kurslar uchun serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


# Darslar uchun serializer
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


# Kommentariyalar uchun serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# Foydalanuvchilar uchun serializer
class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    # Yangi foydalanuvchi yaratish metodi
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# Bildirishnomalar uchun serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'subject', 'message', 'sent']


class LikeLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeLesson
        fields = ['id', 'user', 'lesson', 'created_at']


class DislikeLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DislikeLesson
        fields = ['id', 'user', 'lesson', 'created_at']

