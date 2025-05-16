from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import ValidatorURL
from users.models import Membership


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = '__all__'


class LessonSerialize(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['owner']
        validators = [ValidatorURL(field='video_url')]


class CourseSerialize(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerialize(source="lesson_set", many=True, required=False)
    membership = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [ValidatorURL(field='description')]

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    def get_membership(self, course):
        user = self.context["request"].user
        return Membership.objects.filter(course=course, user=user).exists()





