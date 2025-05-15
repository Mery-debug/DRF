from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User, Membership


class testCRUD(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@sample.ru')
        self.course = Course.objects.create(name='course1', description='test desccription course')
        self.lesson = Lesson.objects.create(name='lesson1', course=self.course, description='test')
        self.membership = Membership.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_create_membership(self):
        url = reverse('users:create_member')
        data = {
            'user': self.user.id,
            'course': self.course.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'message': 'подписка удалена'}

        )

