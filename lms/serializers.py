from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerialize(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerialize(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerialize(source="lesson_set", many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()



