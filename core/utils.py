import jwt

from django.http  import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM
from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):

        if 'Authorization' not in request.headers:
            return JsonResponse({"message": "NEED_LOGIN"}, status=401)

        try:
            jwt_access_token = request.headers['Authorization']
            payload          = jwt.decode(jwt_access_token, SECRET_KEY, algorithms = ALGORITHM)
            login_user       = User.objects.get(id = payload['id'])
            request.user     = login_user

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)

        except jwt.ExpiredSignatureError :
            return JsonResponse({'message':"EXPIRED_TOKEN"}, status=401)

        return func(self, request, *args, **kwargs)
    return wrapper