from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename="courses")

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/list/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<str:pk>/retrieve/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/<str:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/<str:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
] + router.urls



