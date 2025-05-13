from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from lms.serializers import MembershipSerializer
from users.models import User, Payment, Membership


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "city", "img", "is_subscribed", "password",)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        course_id = self.context.get('course_id')

        if request and request.user.is_authenticated:
            return Membership.objects.filter(
                user=request.user,
                course_id=course_id
            ).exists()
        return False


class TokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token

