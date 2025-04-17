from rest_framework import viewsets, generics

from lms.models import Course, Lesson
from lms.serializers import CourseSerialize, LessonSerialize


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerialize
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerialize


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerialize
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerialize
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerialize
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
