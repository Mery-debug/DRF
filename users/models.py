from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Адрес почты")
    img = models.ImageField(
        upload_to="media/img/", blank=True, null=True, verbose_name="Изображение"
    )
    city = models.CharField(null=True, blank=True, verbose_name="Страна")
    phone_number = models.IntegerField(
        null=True, blank=True, help_text="Номер должен содержать только цифры"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return {self.email}

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):

    card = "card"
    cash = "cash"

    payment = [
        (card, "Картой"),
        (cash, "Наличными"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date_payment = models.DateTimeField(null=True, blank=True, verbose_name="Дата оплаты")
    pay_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        blank=True,
        null=True
    )
    pay_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        blank=True,
        null=True
    )
    total_cost = models.IntegerField(null=True, blank=True, verbose_name="Сумма оплаты")
    variation_cost = models.CharField(choices=payment, blank=True, null=True)

    def __str__(self):
        return f"{self.user}, {self.date_payment}, {self.pay_course or self.pay_lesson}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f"{self.user}, {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"



