from django.shortcuts import get_object_or_404
from djoser.conf import User
from rest_framework.request import Request
from rest_framework import viewsets, mixins, status, permissions
from .models import Course, Lesson, Comment, Notification, LikeLesson, DislikeLesson
from .serializers import (CourseSerializer, LessonSerializer, CommentSerializer, UserSerializer, NotificationSerializer,
    LikeLessonSerializer, DislikeLessonSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .utils import send_notification_email
from rest_framework.response import Response


# Foydalanuvchi ruxsatlarini tekshirish uchun maxsus class
class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif view.basename in ['course', 'lesson'] and (request.method in ['POST', 'PUT', 'PATCH', 'DELETE']):
            return request.user and request.user.is_superuser
        else:
            return request.user and request.user


# Kurslar uchun ModelViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CustomPermission]


# Darslar uchun ModelViewSet
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ('title', 'description')    # Dars mavzularini qidirsih
    permission_classes = [CustomPermission]


# Komentariya uchun ModelViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CustomPermission]


# Foydalanuvchilar uchun ViewSet
class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CustomPermission]


# Bildirishnomalar uchun ViewSet
class NotificationViewSet(viewsets.ViewSet, mixins.ListModelMixin):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [CustomPermission]

    # Bildirishnomalarni ro'yxatini qaytarish
    def list(self, request):
        queryset = Notification.objects.all()
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    # Ma'lum bir bildirishnomani qaytarish
    def retrieve(self, request, pk=None):
        notification = get_object_or_404(Notification, pk=pk)
        serializer = self.serializer_class(notification)
        return Response(serializer.data)

    def update(self, request, pk=None):
        notification = get_object_or_404(Notification, pk=pk)
        sent_before_update = notification.sent
        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Yangilanishda sned ni True ga o'zgartirsa habarni jo'natish
            if not sent_before_update and serializer.validated_data.get('sent', False):
                send_notification_email(serializer.instance.id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Yangi bildirishnoma yaratish
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            sent = serializer.validated_data.get('sent', False)

            # Agar bildirishnoma hali jo'natilmagan bo'lsa, saqlab qo'yish
            if not sent:
                serializer.save()
                return Response({"warning": "Yangi habar keyinchalik jo'natish uchun saqlab qolindi."}, status=status.HTTP_400_BAD_REQUEST)

            # Bildirishnomani saqlash va elektron pochta orqali yuborish
            serializer.save()
            send_notification_email(serializer.instance.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeLessonViewSet(viewsets.ModelViewSet):
    queryset = LikeLesson.objects.all()
    serializer_class = LikeLessonSerializer

    def create(self, request, *args, **kwargs):
        lesson_id = request.data.get('lesson')
        existing_dislike = DislikeLesson.objects.filter(lesson=lesson_id, user=request.user).first()

        # Agar foydalanuvchi oldin dislike bosgan bo'lsa uni o'chirib tashlaymiz
        if existing_dislike:
            existing_dislike.delete()
        existing_like = LikeLesson.objects.filter(lesson=lesson_id, user=request.user).first()

        # Agar foydalanuvchi oldin like bosgan bo'lsa uni o'chirib tashlaymiz
        if existing_like:
            existing_like.delete()
            return Response({'message': 'Like o\'chirildi!'}, status=status.HTTP_204_NO_CONTENT)

        # Yangi like yaratamiz
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DislikeLessonViewSet(viewsets.ModelViewSet):
    queryset = DislikeLesson.objects.all()
    serializer_class = DislikeLessonSerializer

    def create(self, request, *args, **kwargs):
        lesson_id = request.data.get('lesson')
        existing_like = LikeLesson.objects.filter(lesson=lesson_id, user=request.user).first()

        # Agar foydalanuvchi oldin like bosgan bo'lsa uni o'chirib tashlash
        if existing_like:
            existing_like.delete()
        existing_dislike = DislikeLesson.objects.filter(lesson=lesson_id, user=request.user).first()

        # Agar foydalanuvchi oldin dislike bosgan bo'lsa uni o'chirib tashlash
        if existing_dislike:
            existing_dislike.delete()
            return Response({'message': 'Dislike o\'chirildi!'}, status=status.HTTP_204_NO_CONTENT)

        # Yangi dislike yaratamiz
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
