from rest_framework.serializers import ValidationError


class OnlySelfAdValidator:
    """Обеспечивает возможность переписки только по поводу своего объявления или объявления получателя."""

    def __init__(self, context):
        self.recipient = context["recipient"]
        self.sender = context["request"].user
        self.ad = context["ad"]

    def __call__(self, data):
        if self.ad.author != self.recipient and self.ad.author != self.sender:
            raise ValidationError("You can only discuss your own advertisement or the recipient's advertisement.")
        if self.recipient == self.sender:
            raise ValidationError("There is no need to send a message to yourself.")
