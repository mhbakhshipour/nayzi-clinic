import re


def is_valid_mobile(value):
    return re.compile(r'^09[0-9]{9}$').search(value)


def is_valid_email(value):
    return re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$").search(value)
