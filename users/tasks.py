from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


def send_verify_email(request, waiting_confirm):
    scheme = request.scheme
    host = request.get_host()
    uid = waiting_confirm.id
    token = waiting_confirm.token
    recipient_list = [waiting_confirm.user.email]
    link = f"{scheme}://{host}/users/verify_email/{uid}/?token={token}"
    subject = "Подтветждение электронной почты."
    message = f"Для подтверждения электронной почты перейдите по ссылке: {link}"
    from_email = EMAIL_HOST_USER
    send_mail(subject, message, from_email, recipient_list)


def send_reset_password_link(request, user, token):
    print(request.get_host())
    print(user)
    print(token)
