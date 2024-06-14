from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CourseViewSet, LessonViewSet, CommentViewSet, UserViewSet, NotificationViewSet, LikeLessonViewSet,
                    DislikeLessonViewSet)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings

# DefaultRouter yordamida URL yo'llarini ro'yxatdan o'tkazish
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'register', UserViewSet)
router.register(r'notification', NotificationViewSet)
router.register(r'likes', LikeLessonViewSet)
router.register(r'dislikes', DislikeLessonViewSet)

# API hujjatlari uchun schema_view yaratish
schema_view = get_schema_view(
    openapi.Info(
        title="Yuna O'quv Markazi API",
        default_version='v1',
        description="Yuna O'quv Markazi loyihasi uchun API hujjatlari",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="maxammadjonov01@bk.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# URL yo'llarini urlpatterns ro'yxatiga qo'shish
urlpatterns = [
    path('', include(router.urls)),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth', include('rest_framework.urls')),

]

# Agar DEBUG True bo'lsa, media fayllar uchun URL yo'llarini qo'shish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)