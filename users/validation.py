import re
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from users.models           import User

REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{10,}$'

def validate_email(email):
    if not re.match(REGEX_EMAIL, email):
        raise ValidationError('INVALID_EMAIL', code=400)

def existing_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError('EMAIL_EXISTS', code=400)

def validate_password(password):
    if not re.match(REGEX_PASSWORD, password):
        raise ValidationError('INVALID_PASSWORD', code=400)