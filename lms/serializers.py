from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import ValidatorURL
from users.models import Membership, Payment


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


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['user', 'pay_course', 'pay_lesson', 'amount', 'variation_cost']

    def validate(self, attrs):
        total_cost = attrs.get('total_cost')
        if total_cost is None:
            raise serializers.ValidationError({
                'total_cost': 'Поле "Сумма оплаты" обязательно для заполнения'
            })
        if total_cost <= 0:
            raise serializers.ValidationError({
                'total_cost': 'Сумма оплаты должна быть больше нуля'
            })
        pay_course = attrs.get('pay_course')
        pay_lesson = attrs.get('pay_lesson')
        if not pay_course and not pay_lesson:
            raise serializers.ValidationError({
                'non_field_errors': ['Необходимо указать либо курс, либо урок']
            })
        if pay_course and pay_lesson:
            raise serializers.ValidationError({
                'non_field_errors': ['Укажите только курс ИЛИ только урок']
            })
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        payment = Payment.objects.create(user=user, **validated_data)
        if not payment.pay_course and not payment.pay_lesson:
            payment.delete()
            raise serializers.ValidationError("Необходимо указать курс или урок")
        return payment


