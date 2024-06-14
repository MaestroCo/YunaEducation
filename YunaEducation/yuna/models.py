from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User


# Kurs modeli
class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Kurs nomi')
    description = models.TextField(verbose_name='Tavsif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan sana')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Yaratuvchi')

    # Ob'ektni strin ko'rinishida qaytarish
    def __str__(self):
        return f'{self.name} - {self.creator}'


# Dars modeli
class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, verbose_name='Kurs')
    title = models.CharField(max_length=255, verbose_name='Dars nomi')
    video_url = models.FileField(upload_to='lesson/videos/', verbose_name='Video fayl', validators=[FileExtensionValidator(
        allowed_extensions=['mp4', 'avi', 'mkv', 'mov']
    )])
    description = models.TextField(blank=True, verbose_name='Tavsif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan sana')

    def __str__(self):
        return f'{self.course} - {self.title}'


# Komentariya modeli
class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE, verbose_name='Dars')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Foydalanuvchi')
    text = models.TextField(verbose_name='Matn')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name='Reyting')

    def __str__(self):
        return f'{self.lesson} - {self.rating}'


# Bildirishnoma modeli
class Notification(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Mavzu')
    message = models.TextField(verbose_name='Xabar')
    sent = models.BooleanField(default=False, verbose_name='Jo\'natish')

    def __str__(self):
        return self.subject


# Yoqtirish modeli
class LikeLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='likes', verbose_name="Yoqdi")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lesson', 'user')

    def __str__(self):
        return f'Like by {self.user} on {self.lesson}'


# Yoqtirmaslik modeli
class DislikeLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='dislikes', verbose_name="Yoqmadi")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lesson', 'user')

    def __str__(self):
        return f'Dislike by {self.user} on {self.lesson}'

