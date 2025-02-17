from unittest.mock import Mock

from users import tasks


def test_send_email_info():
    """Тест отправки уведомлений пользователю"""
    mock_send_mail = Mock(return_value=1)
    tasks.send_mail = mock_send_mail
    tasks.send_email_info("theme", "text", ["user@test.com"])
    mock_send_mail.assert_called_once()


def test_send_email_info_error(capsys):
    """Тест ошибки отправки уведомлений пользователю"""
    mock_send_mail = Mock(side_effect=Exception("Error send mail."))
    tasks.send_mail = mock_send_mail
    tasks.send_email_info("theme", "text", ["user@test.com"])
    captured = capsys.readouterr()
    mock_send_mail.assert_called_once()
    assert captured.err == "Error send mail.\n"
