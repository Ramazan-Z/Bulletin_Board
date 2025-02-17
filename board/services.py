from django.urls import reverse

from users.tasks import send_email_info


def send_message(serializer):
    """Отправка сообщения получателю."""
    scheme = serializer.context["request"].scheme
    host = serializer.context["request"].get_host()
    sender = serializer.context["request"].user
    recipient_list = [serializer.context["recipient"].email]
    ad = serializer.context["ad"]
    message = serializer.validated_data.get("message")
    backlink = f"{scheme}://{host}{reverse('board:send_message', args=[sender.pk, ad.pk])}"
    subject = f"Сообщение от {sender.username} по объявлению «{ad.title}» (id {ad.pk})."
    message = f"{message}\n\nВы можете ответить по ссылке:\n{backlink}."

    send_email_info.delay(subject, message, recipient_list)
