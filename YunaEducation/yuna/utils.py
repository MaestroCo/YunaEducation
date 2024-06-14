from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import Notification


# Bildirishnomalarni foydalanuvchilarga jo'natish uchun funksiya
def send_notification_email(notification_id):
    notification = Notification.objects.get(id=notification_id)
    users = User.objects.all()
    # Barcha foydalanuvchilarni olish va ularni email manzili bor yoki yo'qlikga tekshirish
    for user in users:
        if user.email:
            send_mail(
                notification.subject,
                notification.message,
                'murodjonali25@gmail.com',
                [user.email],
                fail_silently=False,
            )
    notification.sent = True
    notification.save()


def validate_password(password):
    # Parol uzunligi, raqam, katta harf, kichik harf va maxsus belgi mavjudligini tekshirish
    if (len(password) < 8 or not any(char.isdigit() for char in password) or
        not any(char.isupper() for char in password) or not any(char.islower() for char in password) or
            not any(not char.isalnum() for char in password)):
        raise ValidationError(
            "Parol kamida 8 ta belgidan iborat bo'lishi kerak, unda kamida bitta raqam, "
            "bitta katta harf, bitta kichik harf va bitta maxsus belgi bo'lishi shart!"
        )

