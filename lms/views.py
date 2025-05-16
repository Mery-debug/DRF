from rest_framework import viewsets, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.models import Course, Lesson
from lms.paginators import Pagination
from lms.serializers import CourseSerialize, LessonSerialize
from users.permissions import IsManager


@permission_classes([IsAuthenticated])
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerialize
    queryset = Course.objects.all()
    pagination_class = Pagination

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

    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = CourseSerialize(
            course,
            context={'request': request, 'course_id': course.id}
        )
        return Response(serializer.data)

    def get(self, request):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerialize(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerialize
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


@permission_classes([IsAuthenticated])
class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerialize
    queryset = Lesson.objects.all()
    pagination_class = Pagination

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
