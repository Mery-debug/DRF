from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from lms.models import Course, Lesson

User = get_user_model()


class LessonCreationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@sample.ru')
        self.course = Course.objects.create(name='course1', description='test desccription course')
        self.lesson = Lesson.objects.create(name='lesson1', course=self.course, description='test')
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест просмотра урока"""
        url = reverse('lms:lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            {'id': 4, 'name': 'lesson1', 'description': 'test', 'preview': None, 'course': 3}
        )

    def test_lesson_delete(self):
        """Тест удаления урока"""
        url = reverse('lms:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_lesson_create(self):
        """Тест создания урока"""
        url = reverse('lms:lesson_create')
        data = {
            'name': 'lesson2',
            'course': self.course.id,
            'description': 'test description',
            'video_url': 'https://www.youtube.com/watch?v=N1-_EAxsGvA'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': 2, 'name': 'lesson2', 'description': 'test description', 'preview': None, 'course': 1}
        )

    def test_update_lesson(self):
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {
            'name': 'lesson2',
            'course': self.course.id,
            'description': 'test',
            'video_url': 'https://www.youtube.com/watch?v=N1-_EAxsGvA'
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_lesson(self):
        url = reverse('lms:lesson_list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None,
             'results': [{'id': 5, 'name': 'lesson1', 'description': 'test', 'preview': None, 'course': 4}]}

        )



