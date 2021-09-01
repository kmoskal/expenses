import datetime
import jwt
import random
import string
from django.conf import settings


def generate_access_token(custom_user):
    access_token_payload = {
        'user_id': custom_user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,
                                                               minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(custom_user):
    refresh_token_payload = {
        'user_id': custom_user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_token_payload,
                               settings.SECRET_KEY, algorithm='HS256')
    return refresh_token


def generate_activation_token():
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(30))
