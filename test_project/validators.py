from django.core.exceptions import ValidationError
from .models import User

def check_if_email_exist_validator(value):
    if User.objects.filter(email=value).count() != 1:
        raise ValidationError('Email doesnt exist')

def name_validator(value):
    if len(value) < 2:
        raise ValidationError('Name is too short')

def phone_number_validator(value):
    if len(value) < 8:
        raise ValidationError('Your phone number is invalid')

def check_if_is_email_verified(value):
    if User.objects.filter(email=value).count() == 1:
        user = User.objects.get(email=value)
        if user.email_verified is False:
            raise ValidationError('Email is not confirmed')


def password_validator(value):
    if len(value) < 8:
        raise ValidationError('Your password should be obscure and must be at least 8 characters long. In addition, you must have at least one number and a special character within the first ...')