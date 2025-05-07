from rest_framework import viewsets, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerialize, LessonSerialize
from users.permissions import IsManager


@permission_classes([IsAuthenticated])
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerialize
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = (~IsManager,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsManager,)
        return super().get_permissions()



@permission_classes([IsAuthenticated])
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerialize

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


@permission_classes([IsAuthenticated])
class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerialize
    queryset = Lesson.objects.all()


@permission_classes([IsAuthenticated])
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerialize
    queryset = Lesson.objects.all()


@permission_classes([IsAuthenticated])
class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerialize
    queryset = Lesson.objects.all()


@permission_classes([IsAuthenticated])
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
