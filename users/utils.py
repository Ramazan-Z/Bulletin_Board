import re

phone_pattern = re.compile(r"(\+7|8)[\s(\-]?(\d{3,5}?)[\s)\-]?(\d{1,3})[\s\-]?(\d{2})[\s\-]?(\d{2})")


def normalize_phone(phone_number):
    """Преобразование номера телефона к единому виду"""
    if phone_number:
        match = phone_pattern.findall(phone_number)
        if match:
            return f"+7({match[0][1]}){match[0][2]}-{match[0][3]}-{match[0][4]}"
