from rest_framework.serializers import ValidationError


class URLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = 'youtube.com'
        val = dict(value).get(self.field)
        if val:
            if link not in val:
                raise ValidationError('Недопустимая ссылка, разрешена только на youtube.com')
