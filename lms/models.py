
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название курса")
    preview = models.ImageField(upload_to="media/img/", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Обновление курса")

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField()
    preview = models.ImageField(upload_to="media/img/", blank=True, null=True, verbose_name="Превью")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    video_url = models.CharField(null=True, blank=True, verbose_name="ссылка на видео-материал")

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ['name']

