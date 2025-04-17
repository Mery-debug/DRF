from rest_framework import serializers

from lms.models import Course, Lesson


class CourseSerialize(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerialize(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

