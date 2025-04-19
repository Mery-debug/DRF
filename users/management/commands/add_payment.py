from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Payment
from lms.models import Lesson, Course


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user_1, created = User.objects.get_or_create(
            email='sample@example.com',
            defaults={'email': 'sample@example.com', 'password': '123'}
        )
        user_2, created = User.objects.get_or_create(
            email='sample1@example.com',
            defaults={'email': 'sample1@example.com', 'password': '123'}
        )
        course_1, created = Course.objects.get_or_create(name='Курс')
        lesson_1, created = Lesson.objects.get_or_create(name='Урок', course=course_1)

        Payment.objects.create(
            user=user_1,
            pay_course=course_1,
            date_payment="2024-12-12 12:22",
            total_cost=1223.00,
            variation_cost='cash'
        )
        Payment.objects.create(
            user=user_2,
            pay_lesson=lesson_1,
            date_payment="2024-11-12 02:02",
            total_cost=5432.00,
            variation_cost='card'
        )

        self.stdout.write(self.style.SUCCESS('Платежи прошли'))

