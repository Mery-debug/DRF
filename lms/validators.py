import re

from rest_framework.serializers import ValidationError


class ValidatorURL:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r"[https://www.youtube.com/]|[youtube.com/]\d|\D")
        dct = dict(value).get(self.field)
        if not bool(reg.match(dct)):
            raise ValidationError("You are trying to add an invalid URL")

