from django.urls import reverse

from users.tasks import send_email_info


def send_verify_email(request, waiting_confirm):
    """Отправка данных подтверждения электронной почты."""
    scheme = request.scheme
    host = request.get_host()
    uid = waiting_confirm.id
    token = waiting_confirm.token
    if waiting_confirm.new_email:
        recipient_list = [waiting_confirm.new_email]
    else:
        recipient_list = [waiting_confirm.user.email]
    link = f"{scheme}://{host}{reverse('users:verify-email', args=[uid])}?token={token}"
    subject = "Подтветждение адреса электронной почты."
    message = f"Для подтверждения электронной почты перейдите по ссылке: {link}."
    send_email_info.delay(subject, message, recipient_list)


def send_reset_password_info(request, user, token):
    """Отправка данных подтверждения сброса пароля."""
    scheme = request.scheme
    host = request.get_host()
    uid = user.pk
    recipient_list = [user.email]
    reset_password_info = f"{scheme}://{host}{reverse('users:reset-password-confirm')}{uid}/{token}/"
    subject = "Данные для сброса пароля."
    message = f"Для сброса пароля используйте следующие данные: {reset_password_info}"
    send_email_info.delay(subject, message, recipient_list)
