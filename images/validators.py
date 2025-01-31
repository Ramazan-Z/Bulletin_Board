from rest_framework.serializers import ValidationError


class ImageValidator:
    """Исключает возможность добавления изображений к чужим объявлениям"""

    def __init__(self, context):
        self.request = context.get("request")

    def __call__(self, data):
        if data.get("ad").author != self.request.user:
            raise ValidationError("Specify your ad.")
