import re

from rest_framework.serializers import ValidationError


def phone_number_validator(phone_number):
    """Валидатор номера телефона"""
    phone_pattern = re.compile(r"(\+7|8)[\s(\-]?(\d{3,5}?)[\s)\-]?(\d{1,3})[\s\-]?(\d{2})[\s\-]?(\d{2})")
    match = phone_pattern.findall(phone_number)
    if not match:
        raise ValidationError("Incorrect phone number format")
